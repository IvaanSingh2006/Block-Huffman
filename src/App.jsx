import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [blockSize, setBlockSize] = useState(1);
  const [status, setStatus] = useState("");

  const handleCompress = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    setStatus("Compressing...");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("block_size", blockSize);

    try {
      const res = await fetch("https://block-huffman.onrender.com/compress", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Compression failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "compressed.bin";
      a.click();

      setStatus("Compression successful");
    } catch (err) {
      console.error(err);
      setStatus("Error during compression");
    }
  };

  const handleDecompress = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    setStatus("Decompressing...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("https://block-huffman.onrender.com/decompress", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Decompression failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "decompressed_file";
      a.click();

      setStatus("Decompression successful");
    } catch (err) {
      console.error(err);
      setStatus("Error during decompression");
    }
  };

  return (
    <div className="container">
      <h1>Enhanced Huffman Compressor</h1>
      <p>Only use small and simple files for compression</p>
      <p>First compression may take time due to backend inactivity</p>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div style={{ marginTop: "20px" }}>
        <label>Block Size: </label>
        <select
          value={blockSize}
          onChange={(e) => setBlockSize(e.target.value)}
        >
          <option value="1">Normal Huffman</option>
          <option value="2">Block Size 2</option>
          <option value="3">Block Size 3</option>
        </select>
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleCompress}>
          Compress File
        </button>

        <button
          onClick={handleDecompress}
          style={{ marginLeft: "10px" }}
        >
          Decompress File
        </button>
      </div>

      <p style={{ marginTop: "20px" }}>{status}</p>
    </div>
  );
}

export default App;