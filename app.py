from flask import Flask, request, jsonify
import subprocess
import os
from algorithm import *
from time_comp import *

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/run-c-code", methods=["POST"])
def run_c_code():
    try:
        data = request.json
        code = data["code"]
        input_data = data["input"]

        with open("temp.c", "w") as f:
            f.write(code)

        with open("input.txt", "w") as f:
            f.write(input_data)

        compile_process = subprocess.run(
            ["gcc", "temp.c", "-o", "temp"], capture_output=True
        )
        if compile_process.returncode != 0:
            error_message = compile_process.stderr.decode("utf-8")
            cleanup_files(["temp.c", "input.txt", "temp"])
            return jsonify({"output": error_message})

        execution_process = subprocess.run(
            ["./temp"], capture_output=True, input=input_data.encode()
        )
        output = execution_process.stdout.decode("utf-8")

        cleanup_files(["temp.c", "input.txt", "temp"])

        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)})


def cleanup_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)


@app.route("/get-code", methods=["POST"])
def get_code():
    try:
        data = request.json
        algoName = data["algoName"]
        code = get_algorithm(algoName)
        return jsonify({"output": code})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/time-comp", methods=["POST"])
def time_comp():
    try:
        data = request.json
        code = data["code"]
        result = get_time(code)
        return jsonify({"output": result})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
