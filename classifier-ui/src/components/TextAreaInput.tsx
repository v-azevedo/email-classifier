type Props = {
  onChange: (text: string) => void;
  value: string;
};

const TextAreaInput = ({ onChange, value }: Props) => {
  return (
    <div className="flex-3 bg-white border border-gray-200 rounded-3xl p-4">
      <textarea
        className="w-full h-full font-quicksand-400"
        placeholder="Input your text here..."
        value={value}
        onChange={(input) => onChange(input.currentTarget.value)}
        maxLength={10000}
      />
    </div>
  );
};

export default TextAreaInput;
