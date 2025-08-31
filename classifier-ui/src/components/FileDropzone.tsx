import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { IoCloudDone, IoCloudUpload, IoArchive, IoCloseCircle } from "react-icons/io5";

type Props = {
  onFileUpload: (file: File) => void;
  loading: boolean;
  file?: File;
};

const FileDropzone = ({ loading, file, onFileUpload }: Props) => {
  const [fileAccepted, setFileAccepted] = useState("");

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles) {
        onFileUpload(acceptedFiles[0]);
        setFileAccepted(acceptedFiles[0].name);
      }
    },
    [onFileUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "text/plain": [".txt"],
    },
    disabled: loading || (!!fileAccepted && !!file),
    maxFiles: 1,
    maxSize: 2 * 1024 * 1024, // 2MB in bytes
  });

  return (
    <div
      className="relative flex-3 border border-gray-200 p-3 text-center rounded-3xl items-center justify-center bg-white"
      {...getRootProps()}
    >
      {fileAccepted && file && (
        <IoCloseCircle
          onClick={() => setFileAccepted("")}
          className="size-14 absolute -top-5 -right-5 text-primary hover:text-secondary transition-all cursor-pointer"
        />
      )}
      <div className="flex h-full justify-center items-center border-2 border-primary border-dashed rounded-3xl text-primary hover:text-secondary hover:border-secondary">
        <input {...getInputProps()} />
        {isDragActive ? (
          <div className="flex flex-col items-center gap-2">
            <IoArchive className="size-16" />
            <p className="font-quicksand-600">Drop the file here...</p>
          </div>
        ) : fileAccepted && file ? (
          <div className="flex flex-col items-center gap-2">
            <IoCloudDone className="size-16" />
            <p className="font-quicksand-600">{fileAccepted}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2 font-quicksand-400">
            <IoCloudUpload className="size-16" />
            <p className="font-quicksand-600">Choose a file or drag it here!</p>
            <p className="text-sm text-gray-400">Supported files: PDF, TXT</p>
            <p className="text-sm text-gray-400">Max size: 2MB</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileDropzone;
