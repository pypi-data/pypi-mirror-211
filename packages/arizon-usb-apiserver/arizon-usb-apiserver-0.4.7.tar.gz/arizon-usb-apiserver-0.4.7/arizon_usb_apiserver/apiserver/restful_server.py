import argparse
import logging
import time

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from arizon_usb_apiserver import Config as SensorConfig
from .app import Application

controller = FastAPI()

controller.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APPLICATION: Application = None


def make_response(status_code, **kwargs):
    data = {'code': status_code, 'timestamp': time.time()}
    data.update(**kwargs)
    json_compatible_data = jsonable_encoder(data)
    resp = JSONResponse(content=json_compatible_data, status_code=status_code)
    return resp


@controller.get("/")
def root():
    return RedirectResponse(url='/docs')


@controller.get("/v1/arizon/status")
def get_status():
    global APPLICATION
    if APPLICATION.fifo_status:
        return make_response(200, message="force data collection is running", status=True)
    else:
        return make_response(200, message="force data collection is stopped", status=False)


@controller.get("/v1/arizon/force")
def get_force():
    global APPLICATION
    return make_response(200, data=APPLICATION.get())


@controller.delete("/v1/arizon/force")
def clean_cached_force():
    global APPLICATION
    APPLICATION.clean_cached_force()
    return make_response(200, message="force data queue cleaned")


@controller.put("/v1/arizon/force")
def toggle_force(flag: bool):
    global APPLICATION
    if flag:
        APPLICATION.start_fifo()
    else:
        APPLICATION.stop_fifo()
    return make_response(200, message="force data collection {}".format("started" if APPLICATION.fifo_status else "stopped"), status=flag)


@controller.post("/v1/arizon/start")
def start_recording(tag: str):
    global APPLICATION
    ret = APPLICATION.start_recording(tag)
    return make_response(200, message="force data collection started", status=True, ret=str(ret))


@controller.post("/v1/arizon/stop")
def stop_recording():
    global APPLICATION
    ret = APPLICATION.stop_recording()
    return make_response(200, message="force data collection stopped", status=False, ret=str(ret))


def main(args):
    global APPLICATION
    logging.basicConfig(level=logging.INFO)

    cfg = SensorConfig(args.config)
    if cfg.valid is False:
        logging.error(f"invalid config file {args.config}")
        exit(1)
    APPLICATION = Application(cfg)

    # Prepare system
    APPLICATION.logger.info(f"arizon sensor service listen at {cfg.api_port}")
    APPLICATION.logger.info(f"arizon sensor config {cfg}")

    APPLICATION.start_thread()

    try:
        # app.run(host='0.0.0.0', port=api_port)
        uvicorn.run(app=controller, port=cfg.api_port, host=cfg.api_interface)
    except KeyboardInterrupt:
        APPLICATION.logger.info(f"got KeyboardInterrupt")
        return


def entry_point(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./arizon_config.yaml")
    run_args = parser.parse_args(argv)
    main(run_args)


if __name__ == '__main__':
    import sys
    exit(entry_point(sys.argv[1:]))
