import { Bounce, ToastContainer, toast } from "react-toastify";
import { FaArrowsUpDown } from "react-icons/fa6";
import { useState } from "react";
import axios from "axios";

import "./App.css";
import Instructions from "./components/Instructions";
import Header from "./components/Header";
import FileDropzone from "./components/FileDropzone";
import Button from "./components/Button";
import Classification from "./components/Classification";
import TextAreaInput from "./components/TextAreaInput";

type ResultType = {
  classification: string;
  reply: string;
};

function App() {
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File>();
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<ResultType>();

  const handleFile = (file: File) => {
    setFile(file);
  };

  const handleInput = (text: string) => {
    setInput(text);
  };

  const handleClassification = async () => {
    try {
      let data: ResultType | undefined = undefined;
      setIsLoading(true);

      if (file) {
        data = (await axios.postForm("https://email-classifier-t597.onrender.com/classify-upload", { file: file }))
          .data;
      } else if (input) {
        data = (await axios.post("https://email-classifier-t597.onrender.com/classify-text", { text: input })).data;
      }

      if (data) {
        setResponse(data);
      }
    } catch (e) {
      toast.error("There was a problem with the request, try again.");
      console.log(e);
    } finally {
      setIsLoading(false);
      setFile(undefined);
    }
  };

  const handleReply = () => {};

  const resetForm = () => {
    setIsLoading(false);
    setResponse(undefined);
  };

  return (
    <>
      <div className="fixed bg-secondary rounded-full w-[74vh] h-[74vh] -z-50 -right-36 -top-72" />
      <div className="fixed bg-secondary rounded-full w-[140vh] h-[140vh] -z-50 -left-48 -bottom-[36rem]" />
      <Header />
      <div className="grid grid-cols-12 w-full pt-24 h-[75%] px-10">
        <div className="flex justify-between flex-col col-span-5">
          <FileDropzone loading={isLoading} onFileUpload={handleFile} file={file} />
          <div className="flex flex-1 justify-center items-center">
            <FaArrowsUpDown className="size-8 text-primary" />
          </div>
          <TextAreaInput value={input} onChange={handleInput} />
        </div>
        <div className="col-span-2 flex justify-center items-center">
          <Button loading={isLoading} onClickPrimary={handleClassification} onClickSecondary={handleReply} />
        </div>
        <section className="relative flex flex-1 col-span-5">
          {response ? (
            <Classification
              loading={isLoading}
              classification={response.classification}
              reply={response.reply}
              onReset={resetForm}
            />
          ) : (
            <Instructions loading={isLoading} />
          )}
        </section>
      </div>
      <footer className="mt-10">
        <p className="font-quicksand-200 text-gray-400 text-sm text-right">Made by: Victor Azevedo</p>
      </footer>
      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
        transition={Bounce}
      />
    </>
  );
}

export default App;
