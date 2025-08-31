import clsx from "clsx";

type Props = {
  loading: boolean;
  onClickPrimary: () => void;
  onClickSecondary: () => void;
};

const Button = ({ loading, onClickPrimary, onClickSecondary }: Props) => {
  return (
    <div className="flex flex-col h-44 justify-between">
      <button
        type="button"
        disabled={loading}
        onClick={onClickPrimary}
        className={clsx(
          "w-full h-full p-2 cursor-pointer rounded-t-full bg-primary text-white enabled:hover:bg-white enabled:hover:text-gray-700 transition",
          loading && "opacity-20"
        )}
      >
        <p className="font-quicksand-800">Classify</p>
      </button>
      <div className="border-b-2 border-white"></div>
      <button
        type="button"
        disabled={loading}
        onClick={onClickSecondary}
        className={clsx(
          "w-full h-full p-2 cursor-pointer rounded-b-full bg-primary text-white enabled:hover:bg-white enabled:hover:text-gray-700 transition",
          loading && "opacity-20"
        )}
      >
        <p className="font-quicksand-800">Reply</p>
      </button>
    </div>
  );
};

export default Button;
