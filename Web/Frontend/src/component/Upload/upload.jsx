import { useState, useContext, useEffect } from "react";
// import AuthContext from "../../context/AuthContext"; // giả sử bạn đã thiết lập AuthContext
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AxiosInstance from "../AxiosInstance";

export default function Upload() {
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

  useEffect(() => {
    AxiosInstance.get(``)
      .then((res) => setfilesUpload(res.data))
      .catch((err) => console.log(err));
  }, []);

  const handleShow = (id) => {
    setSelectedCard(selectedCard === id ? null : id);
  };

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
      const file = event.target.files[0];
      if (file) {
        // Lưu trữ các thuộc tính tệp vào state
        setFileInfo({
          name: file.name,
          size: (file.size / (1024 * 1024)).toFixed(2) + " MB", // Kích thước tính bằng MB
          type: file.type,
          lastModified: new Date(file.lastModified).toLocaleDateString(),
        });
      }
    } else {
      setFile(null);
      toast.error("No file selected. Please choose a file to upload.");
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
          {/* <button className="btn btn-primary">
            Add torrent <i className="bi bi-plus"></i>
          </button> */}
        </div>
      </div>

      <div className="d-flex flex-column align-items-center justify-content-center px-1 my-3">
        <div className="w-100 rounded-4 bg-white border shadow">
          {filesUpload.map((d) => (
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
                      <div>{new Date(d.dateAdd).toLocaleDateString()}</div>
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
          ))}
        </div>
      </div>

      {/* Modal */}
      <div
        className="modal fade"
        id="createTorrentModal"
        tabIndex="-1"
        aria-labelledby="createTorrentModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="createTorrentModalLabel">
                Create torrent
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="form-control mb-3"
                />
                {/* <p className="text-muted">
                  C:\Users\Do Truong Khoa\Downloads\6_SQL_update_2024.pdf
                </p> */}
                <p>{file && "1 File, " + fileInfo.size}</p>
              </div>
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
              {/* <div className="form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="startSeeding"
                />
                <label className="form-check-label" for="startSeeding">
                  Start seeding when created
                </label>
              </div> */}
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleGenerateTorrent}
              >
                Create torrent
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
