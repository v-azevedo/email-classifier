import { FaArrowRotateRight } from "react-icons/fa6";
import { RotateLoader } from "react-spinners";

type Props = {
  classification: string;
  reply?: string;
  loading: boolean;
  onReset: () => void;
};

const Classification = ({ classification, reply, loading, onReset }: Props) => {
  return (
    <>
      <div
        onClick={onReset}
        className="absolute flex h-12 w-12 top-5 right-5 bg-secondary rounded-full justify-center items-center cursor-pointer hover:scale-110 transition-all"
      >
        <FaArrowRotateRight className="size-5 text-white" />
      </div>
      <div className="absolute h-12 w-12 bottom-5 left-5 bg-secondary rounded-full"></div>
      <div className="w-full border border-gray-200 py-6 px-10 rounded-3xl bg-white flex flex-col gap-8">
        {loading ? (
          <div className="flex flex-col justify-center items-center flex-1 gap-10">
            <RotateLoader color="#5500ff" />
            <p className="font-quicksand-600 text-gray-400">Reading file and classifying...</p>
          </div>
        ) : (
          <>
            <div className="font-quicksand-400 flex flex-col gap-5 mb-8">
              <h1 className="text-center font-quicksand-700 text-primary text-xl">Classification</h1>
              <p className="text-xl text-center">{classification}</p>
            </div>
            <div className="border-b border-gray-200 mb-8" />
            {reply && (
              <div className="font-quicksand-400 flex flex-col gap-5 mb-1">
                <h1 className="text-center font-quicksand-700 text-primary text-xl">Reply</h1>
                <p className="text-xl tracking-wide">{reply}</p>
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
};

export default Classification;
