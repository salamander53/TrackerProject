import { useState, useContext, useEffect } from "react";
// import AuthContext from "../../context/AuthContext"; // giả sử bạn đã thiết lập AuthContext
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AxiosInstance from "../AxiosInstance";
import parseTorrent from "parse-torrent";
import { Buffer } from "buffer"; // Import Buffer từ thư viện buffer
import bencode from "bencode";

export default function Home() {
  const [filesUpload, setfilesUpload] = useState([
    {
      id: 1,
      name: "file 1",
      dateAdd: Date.now(),
      totalFile: 2,
      totalSize: "100mb",
    },
    {
      id: 2,
      name: "file 2",
      dateAdd: Date.now(),
      totalFile: 2,
      totalSize: "100mb",
    },
  ]);
  const [selectedCard, setSelectedCard] = useState(null);
  // const [showModal, setShowModal] = useState(false);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);
  // const { user } = useContext(AuthContext);

  // useEffect(() => {
  //   AxiosInstance.get(``)
  //     .then((res) => {
  //       if (Array.isArray(res.data)) {
  //         setfilesUpload(res.data);
  //       } else {
  //         console.error("Unexpected response format:", res.data);
  //       }
  //     })
  //     .catch((err) => console.error("Error fetching data:", err));
  // }, []);

  const handleShow = (id) => {
    setSelectedCard(selectedCard === id ? null : id);
  };

  function readFileContent(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
        resolve(reader.result); // Nội dung file sau khi đọc xong
      };

      reader.onerror = () => {
        reject(reader.error); // Lỗi nếu xảy ra trong quá trình đọc file
      };

      // Đọc file dưới dạng text (có thể đổi thành ArrayBuffer nếu cần)
      reader.readAsText(file);
    });
  }

  const handleFileChange = (event) => {
    // console.log(event.target.files[0]);
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
      // const file = event.target.files[0];
      // if (file) {
      //   // Lưu trữ các thuộc tính tệp vào state
      //   setFileInfo({
      //     name: file.name,
      //     size: (file.size / (1024 * 1024)).toFixed(2) + " MB", // Kích thước tính bằng MB
      //     type: file.type,
      //     lastModified: new Date(file.lastModified).toLocaleDateString(),
      //   });
      // }
    } else {
      setFile(null);
      toast.error("No file selected. Please choose a file to upload.");
    }
  };

  const getPiecesArray = (piecesBuffer) => {
    const pieceLength = 20; // Mỗi hash dài 20 byte
    const piecesArray = [];

    for (let i = 0; i < piecesBuffer.length; i += pieceLength) {
      const piece = piecesBuffer.slice(i, i + pieceLength);
      piecesArray.push(Buffer.from(piece).toString("hex")); // Chuyển thành chuỗi hex
    }

    return piecesArray;
  };

  const handleAddTorrent = async (event) => {
    event.preventDefault();

    if (!file) {
      toast.error("No file selected. Please choose a file to upload.");
      return;
    }

    try {
      const arrayBuffer = await file.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);

      // Giải mã bencode
      const decodedData = bencode.decode(buffer);

      // Chuyển đổi Uint8Array sang chuỗi
      const announce = new TextDecoder().decode(decodedData.announce);
      const name = new TextDecoder().decode(decodedData.info.name);
      const pieces = new TextDecoder().decode(decodedData.info.pieces);

      console.log("Decoded Torrent File:", {
        announce,
        name,
        pieces,
      });

      // Tạo FormData
      const formData = new FormData();

      // Thêm dữ liệu vào FormData
      formData.append("title", name); // Tiêu đề (chuỗi)
      formData.append("announce", announce); // URL của tracker (chuỗi)
      formData.append("file_length", decodedData.info.length); // Kích thước file (số nguyên lớn)
      formData.append("piece_length", decodedData.info["piece length"]); // Kích thước mỗi mảnh (số nguyên)
      formData.append(
        "pieces",
        JSON.stringify(getPiecesArray(Buffer.from(decodedData.info.pieces)))
      ); // Dữ liệu băm của các mảnh (hex string)

      console.log("FormData:", formData);

      // Gửi FormData lên server
      const res = await AxiosInstance.post("torrents/", formData);
      console.log(res);
      toast.success("File uploaded successfully!");
    } catch (error) {
      console.error("Error decoding torrent file:", error);
      toast.error("Failed to process the file. Please try again.");
    }
  };

  const handleGenerateTorrent = async () => {
    if (!file) {
      toast.error("No file selected. Please choose a file to upload.");
      return;
    }
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("torrentName", file.name);

    try {
      const response = await AxiosInstance.post(``, formData);
      console.log(response);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error ||
            "An error occurred while generating the torrent file."
        );
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = `${file.name}.torrent`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
      toast.success("Torrent file generated successfully!");
    } catch (error) {
      toast.error(error.message || "An error occurred.");
    } finally {
      setUploading(false);
      // setShowModal(false);
    }
  };
  return (
    <>
      <ToastContainer />
      <div
        className="d-flex flex-column align-items-center justify-content-center mb-4"
        style={{ paddingTop: 20 }}
      >
        <div className="w-100 rounded bg-white border shadow " style={{}}>
          <div className="d-flex justify-content-between align-items-center px-2 py-2 text-dark">
            <div className="d-flex gap-2">
              <button className="btn btn-outline-secondary d-flex align-items-center">
                <i className="bi bi-grid-3x3-gap me-1"></i>
                <i className="bi bi-chevron-down"></i>
              </button>
              <button className="btn btn-outline-secondary dropdown-toggle">
                Show: All
              </button>
              <button className="btn btn-outline-secondary dropdown-toggle">
                Sort: Most Recent
              </button>
            </div>
            <div className="d-flex gap-2">
              <button
                className="btn btn-outline-secondary"
                data-bs-toggle="modal"
                data-bs-target="#createTorrentModal"
              >
                Create torrent <i className="bi bi-plus"></i>
              </button>
              <button
                className="btn btn-outline-secondary"
                data-bs-toggle="modal"
                data-bs-target="#addTorrentModal"
              >
                Add torrent <i className="bi bi-plus"></i>
              </button>
            </div>
          </div>

          <div className="d-flex flex-column align-items-center justify-content-center px-1 my-3">
            <div className="w-100 rounded-4 bg-white border shadow">
              {/* {Array.isArray(filesUpload) &&
                filesUpload.map((d, i) => (
                  <div key={d.id} className="my-3 border-bottom">
                    <div className="d-flex align-items-center p-3">
                      <div className="flex-shrink-0 me-3">
                        <i
                          className="bi bi-upload"
                          style={{ fontSize: "1.5rem" }}
                        ></i>
                      </div>
                      <div className="flex-grow-1">
                        <h5 className="mb-0">{d.name}</h5>
                        <div className="d-flex align-items-center mt-1">
                          <span className="badge bg-success me-2">Seeding</span>
                          <span className="text-muted">0 B/s</span>
                        </div>
                      </div>
                      <div className="d-flex gap-2">
                        <button className="btn btn-outline-dark btn-sm">
                          <i className="bi bi-share"></i>
                        </button>
                        <button className="btn btn-outline-dark btn-sm">
                          <i className="bi bi-folder"></i>
                        </button>
                        <button className="btn btn-outline-dark btn-sm">
                          <i className="bi bi-trash"></i>
                        </button>
                        <button
                          className="btn btn-outline-dark btn-sm"
                          onClick={() => handleShow(d.id)}
                        >
                          <i className="bi bi-info-circle"></i>
                        </button>
                      </div>
                    </div>
                    {selectedCard === d.id && (
                      <div className="bg-light p-3 rounded-bottom">
                        <div className="d-flex justify-content-between">
                          <div>
                            <strong>Date Added</strong>
                            <div>
                              {new Date(d.dateAdd).toLocaleDateString()}
                            </div>
                            <strong>Total Files</strong>
                            <div>{d.totalFile} File</div>
                            <strong>Total Size</strong>
                            <div>{d.totalSize}</div>
                          </div>
                          <div className="d-flex flex-column align-items-center">
                            <strong>Torrent files</strong>
                            <span className="text-muted">{d.name}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))} */}
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      <div
        className="modal fade"
        id="addTorrentModal"
        tabindex="-1"
        aria-labelledby="addTorrentModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="addTorrentModalLabel">
                Adding 1 Torrent
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">
              <div>
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="form-control mb-3"
                  accept=".torrent"
                />
                {/* <p>{file && "1 File, " + fileInfo.size}</p> */}
                <p>
                  Peers: 0 | Seeds: 0{" "}
                  <span className="badge bg-warning text-dark">
                    Low peers and seeds
                  </span>
                </p>
              </div>

              {/* <table class="table table-bordered">
                <thead>
                  <tr>
                    <th scope="col">
                      <input type="checkbox" checked />
                      Name
                    </th>
                    <th scope="col">Size</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <input type="checkbox" checked />
                      CSDL (TH) ASSIGNMENT 1.pdf
                    </td>
                    <td>384 KB</td>
                  </tr>
                </tbody>
              </table> */}

              <div class="mb-3">
                <label class="form-label">Download this torrent to:</label>
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control"
                    value="C:\Users\Do Truong Khoa\Downloads"
                    readonly
                  />
                  <button class="btn btn-outline-secondary" type="button">
                    Change
                  </button>
                </div>
              </div>

              {/* <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="startDownload"
                  checked
                />
                <label class="form-check-label" for="startDownload">
                  Start downloading when torrent is added
                </label>
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="dontShowDialog"
                />
                <label class="form-check-label" for="dontShowDialog">
                  Don’t show this dialog next time I add a torrent
                </label>
              </div> */}
            </div>

            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button
                type="button"
                class="btn btn-primary"
                onClick={(e) => handleAddTorrent(e)}
              >
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
