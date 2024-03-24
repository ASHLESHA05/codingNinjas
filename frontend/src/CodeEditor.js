import React, { useRef, useState } from "react";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-c_cpp";
import "ace-builds/src-noconflict/theme-monokai";
import "./CodeEditor.css";
import axios from "axios";

const CodeEditor = () => {
  const [code, setCode] = useState(
    '//write "//Algorithm <algorithm_name>" and press enter to get it\'s code\n#include <stdio.h>\n\nint main() {\n\tprintf("Hello world ");\n\treturn 0;\n}'
  );
  const [output, setOutput] = useState("");
  const [input, setInput] = useState("");
  const [inference, setInference] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("c_cpp");
  const [loading, setLoading] = useState(false);
  const editorRef = useRef(null);
  let timer;

  const runCode = async () => {
    try {
      // Clear previous output
      setOutput("");
      setLoading(true);

      // Send code and input to server for execution
      const response = await axios.post("http://localhost:5000/run-c-code", {
        code,
        input,
      });

      // Parse response and set output
      const result = response.data;
      setOutput(result.output);
    } catch (error) {
      // Handle errors
      console.error("Error running C code:", error);
      setOutput("Error: " + error.toString());
    } finally {
      setLoading(false);
    }
  };

  const sendCodeToBackend = async (codeToSend) => {
    try {
      setLoading(true);
      const response = await axios.post("http://localhost:5000/time-comp", {
        code: codeToSend,
      });

      const result = response.data;
      setInference(result.output);
    } catch (error) {
      console.error("Error running C code:", error);
    } finally {
      setLoading(false);
    }
  };
  
  const onChangeHandler = async (newCode) => {
    setCode(newCode);
    clearTimeout(timer);
    const codeLines = newCode.split("\n");

    codeLines.forEach(async (line, index) => {
      if (line.toLowerCase().includes("//algorithm")) {
        if (codeLines[index + 1] === "") {
          const operationName = line.replace("//", "").trim();
          console.log("Operation:", operationName);
          try {
            setLoading(true);
            const response = await axios.post(
              "http://localhost:5000/get-code",
              { algoName: operationName }
            );
            const result = response.data;
            appendText(result.output);
          } catch (error) {
            console.log(error);
          } finally {
            setLoading(false);
          }
        }
      }
    });

    let lastTypingTime = new Date().getTime();
    timer = setTimeout(() => {
      let timeNow = new Date().getTime();
      var diff = timeNow - lastTypingTime;
      if (diff >= 2000) {
        codeLines.shift();
        const codeToSend = codeLines.join("\n");
        let codeWithoutComment = codeToSend.replace(/\/\/.*$/gm, "");
        codeWithoutComment = codeWithoutComment.replace(
          /\/\*[\s\S]*?\*\//g,
          ""
        );
        if (codeWithoutComment.trim().endsWith("}")) {
          sendCodeToBackend(codeWithoutComment);
        }
      }
    }, 2000);
  };

  const appendText = (textToAppend) => {
    console.log("Appending text:", textToAppend);
    if (editorRef.current && editorRef.current.editor) {
      const editor = editorRef.current.editor;
      const cursorPosition = editor.getCursorPosition();

      editor.session.insert(cursorPosition, textToAppend);
    } else {
      console.log(
        "Editor reference not found or editor instance not available."
      );
    }
  };

  return (
    <>
      <h1 className="heading">C Code Compiler and Analyzer</h1>
      <div className="main">
        <div className="code-editor-container">
          <AceEditor
            height="400px"
            width="900px"
            value={code}
            ref={editorRef}
            mode={selectedLanguage}
            theme="monokai"
            fontSize="16px"
            highlightActiveLine={true}
            onChange={onChangeHandler}
            setOptions={{
              enableLiveAutocompletion: true,
              showLineNumbers: true,
              tabSize: 2,
            }}
          />
          <div className="container">
            <div className="editor-controls">
              <button onClick={runCode}>Run</button>
            </div>
            <div className="input-output">
              <div className="input-container">
                <h3>Input:</h3>
                <textarea
                  className="input"
                  style={{ width: "300px", height: "200px" }}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Enter input here..."
                />
              </div>
              <div className="output-container">
                <h3>Output:</h3>
                <textarea
                  className="output"
                  style={{ width: "550px", height: "200px" }}
                  value={output}
                  placeholder="Output will appear here"
                  readOnly
                />
              </div>
            </div>
          </div>
        </div>
        <div className="observation">
          {loading && <div className="loading">Loading...<div className="loading-spinner"></div></div>}
          <textarea
            className="observation-area"
            style={{
              width: "550px",
              height: "700px",
              marginLeft: "25px",
            }}
            value={inference}
            placeholder="Inference of your code"
            readOnly
          />
        </div>
      </div>
    </>
  );
};

export default CodeEditor;
