import { useState, useContext, useEffect } from "react";
// import AuthContext from "../../context/AuthContext"; // giả sử bạn đã thiết lập AuthContext
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AxiosInstance from "../AxiosInstance";
import parseTorrent from "parse-torrent";
import { Buffer } from "buffer"; // Import Buffer từ thư viện buffer
import bencode from "bencode";

// export default function Home() {
//   const [filesUpload, setfilesUpload] = useState([
//     {
//       id: 1,
//       name: "file 1",
//       dateAdd: Date.now(),
//       totalFile: 2,
//       totalSize: "100mb",
//     },
//     {
//       id: 2,
//       name: "file 2",
//       dateAdd: Date.now(),
//       totalFile: 2,
//       totalSize: "100mb",
//     },
//   ]);
//   const [selectedCard, setSelectedCard] = useState(null);
//   // const [showModal, setShowModal] = useState(false);
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [fileInfo, setFileInfo] = useState(null);
//   // const { user } = useContext(AuthContext);

//   // useEffect(() => {
//   //   AxiosInstance.get(``)
//   //     .then((res) => {
//   //       if (Array.isArray(res.data)) {
//   //         setfilesUpload(res.data);
//   //       } else {
//   //         console.error("Unexpected response format:", res.data);
//   //       }
//   //     })
//   //     .catch((err) => console.error("Error fetching data:", err));
//   // }, []);

//   const handleShow = (id) => {
//     setSelectedCard(selectedCard === id ? null : id);
//   };

//   function readFileContent(file) {
//     return new Promise((resolve, reject) => {
//       const reader = new FileReader();

//       reader.onload = () => {
//         resolve(reader.result); // Nội dung file sau khi đọc xong
//       };

//       reader.onerror = () => {
//         reject(reader.error); // Lỗi nếu xảy ra trong quá trình đọc file
//       };

//       // Đọc file dưới dạng text (có thể đổi thành ArrayBuffer nếu cần)
//       reader.readAsText(file);
//     });
//   }

//   const handleFileChange = (event) => {
//     // console.log(event.target.files[0]);
//     if (event.target.files && event.target.files.length > 0) {
//       setFile(event.target.files[0]);
//       // const file = event.target.files[0];
//       // if (file) {
//       //   // Lưu trữ các thuộc tính tệp vào state
//       //   setFileInfo({
//       //     name: file.name,
//       //     size: (file.size / (1024 * 1024)).toFixed(2) + " MB", // Kích thước tính bằng MB
//       //     type: file.type,
//       //     lastModified: new Date(file.lastModified).toLocaleDateString(),
//       //   });
//       // }
//     } else {
//       setFile(null);
//       toast.error("No file selected. Please choose a file to upload.");
//     }
//   };

//   const getPiecesArray = (piecesBuffer) => {
//     const pieceLength = 20; // Mỗi hash dài 20 byte
//     const piecesArray = [];

//     for (let i = 0; i < piecesBuffer.length; i += pieceLength) {
//       const piece = piecesBuffer.slice(i, i + pieceLength);
//       piecesArray.push(Buffer.from(piece).toString("hex")); // Chuyển thành chuỗi hex
//     }

//     return piecesArray;
//   };

//   const handleAddTorrent = async (event) => {
//     event.preventDefault();

//     if (!file) {
//       toast.error("No file selected. Please choose a file to upload.");
//       return;
//     }

//     try {
//       const arrayBuffer = await file.arrayBuffer();
//       const buffer = Buffer.from(arrayBuffer);

//       // Giải mã bencode
//       const decodedData = bencode.decode(buffer);

//       // Chuyển đổi Uint8Array sang chuỗi
//       const announce = new TextDecoder().decode(decodedData.announce);
//       const name = new TextDecoder().decode(decodedData.info.name);
//       const pieces = new TextDecoder().decode(decodedData.info.pieces);

//       console.log("Decoded Torrent File:", {
//         announce,
//         name,
//         pieces,
//       });

//       // Tạo FormData
//       const formData = new FormData();

//       // Thêm dữ liệu vào FormData
//       formData.append("title", name); // Tiêu đề (chuỗi)
//       formData.append("announce", announce); // URL của tracker (chuỗi)
//       formData.append("file_length", decodedData.info.length); // Kích thước file (số nguyên lớn)
//       formData.append("piece_length", decodedData.info["piece length"]); // Kích thước mỗi mảnh (số nguyên)
//       formData.append(
//         "pieces",
//         JSON.stringify(getPiecesArray(Buffer.from(decodedData.info.pieces)))
//       ); // Dữ liệu băm của các mảnh (hex string)

//       console.log("FormData:", formData);

//       // Gửi FormData lên server
//       const res = await AxiosInstance.post("torrents/", formData);
//       console.log(res);
//       toast.success("File uploaded successfully!");
//     } catch (error) {
//       console.error("Error decoding torrent file:", error);
//       toast.error("Failed to process the file. Please try again.");
//     }
//   };

//   const handleGenerateTorrent = async () => {
//     if (!file) {
//       toast.error("No file selected. Please choose a file to upload.");
//       return;
//     }
//     setUploading(true);

//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append("torrentName", file.name);

//     try {
//       const response = await AxiosInstance.post(``, formData);
//       console.log(response);

//       if (!response.ok) {
//         const errorData = await response.json();
//         throw new Error(
//           errorData.error ||
//             "An error occurred while generating the torrent file."
//         );
//       }

//       const blob = await response.blob();
//       const downloadUrl = window.URL.createObjectURL(blob);
//       const link = document.createElement("a");
//       link.href = downloadUrl;
//       link.download = `${file.name}.torrent`;
//       document.body.appendChild(link);
//       link.click();
//       link.remove();
//       window.URL.revokeObjectURL(downloadUrl);
//       toast.success("Torrent file generated successfully!");
//     } catch (error) {
//       toast.error(error.message || "An error occurred.");
//     } finally {
//       setUploading(false);
//       // setShowModal(false);
//     }
//   };
//   return (
//     <>
//       <ToastContainer />
//       <div
//         className="d-flex flex-column align-items-center justify-content-center mb-4"
//         style={{ paddingTop: 20 }}
//       >
//         <div className="w-100 rounded bg-white border shadow " style={{}}>
//           <div className="d-flex justify-content-between align-items-center px-2 py-2 text-dark">
//             <div className="d-flex gap-2">
//               <button className="btn btn-outline-secondary d-flex align-items-center">
//                 <i className="bi bi-grid-3x3-gap me-1"></i>
//                 <i className="bi bi-chevron-down"></i>
//               </button>
//               <button className="btn btn-outline-secondary dropdown-toggle">
//                 Show: All
//               </button>
//               <button className="btn btn-outline-secondary dropdown-toggle">
//                 Sort: Most Recent
//               </button>
//             </div>
//             <div className="d-flex gap-2">
//               <button
//                 className="btn btn-outline-secondary"
//                 data-bs-toggle="modal"
//                 data-bs-target="#createTorrentModal"
//               >
//                 Create torrent <i className="bi bi-plus"></i>
//               </button>
//               <button
//                 className="btn btn-outline-secondary"
//                 data-bs-toggle="modal"
//                 data-bs-target="#addTorrentModal"
//               >
//                 Add torrent <i className="bi bi-plus"></i>
//               </button>
//             </div>
//           </div>

//           <div className="d-flex flex-column align-items-center justify-content-center px-1 my-3">
//             <div className="w-100 rounded-4 bg-white border shadow">
//               {/* {Array.isArray(filesUpload) &&
//                 filesUpload.map((d, i) => (
//                   <div key={d.id} className="my-3 border-bottom">
//                     <div className="d-flex align-items-center p-3">
//                       <div className="flex-shrink-0 me-3">
//                         <i
//                           className="bi bi-upload"
//                           style={{ fontSize: "1.5rem" }}
//                         ></i>
//                       </div>
//                       <div className="flex-grow-1">
//                         <h5 className="mb-0">{d.name}</h5>
//                         <div className="d-flex align-items-center mt-1">
//                           <span className="badge bg-success me-2">Seeding</span>
//                           <span className="text-muted">0 B/s</span>
//                         </div>
//                       </div>
//                       <div className="d-flex gap-2">
//                         <button className="btn btn-outline-dark btn-sm">
//                           <i className="bi bi-share"></i>
//                         </button>
//                         <button className="btn btn-outline-dark btn-sm">
//                           <i className="bi bi-folder"></i>
//                         </button>
//                         <button className="btn btn-outline-dark btn-sm">
//                           <i className="bi bi-trash"></i>
//                         </button>
//                         <button
//                           className="btn btn-outline-dark btn-sm"
//                           onClick={() => handleShow(d.id)}
//                         >
//                           <i className="bi bi-info-circle"></i>
//                         </button>
//                       </div>
//                     </div>
//                     {selectedCard === d.id && (
//                       <div className="bg-light p-3 rounded-bottom">
//                         <div className="d-flex justify-content-between">
//                           <div>
//                             <strong>Date Added</strong>
//                             <div>
//                               {new Date(d.dateAdd).toLocaleDateString()}
//                             </div>
//                             <strong>Total Files</strong>
//                             <div>{d.totalFile} File</div>
//                             <strong>Total Size</strong>
//                             <div>{d.totalSize}</div>
//                           </div>
//                           <div className="d-flex flex-column align-items-center">
//                             <strong>Torrent files</strong>
//                             <span className="text-muted">{d.name}</span>
//                           </div>
//                         </div>
//                       </div>
//                     )}
//                   </div>
//                 ))} */}
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Modal */}
//       <div
//         className="modal fade"
//         id="addTorrentModal"
//         tabindex="-1"
//         aria-labelledby="addTorrentModalLabel"
//         aria-hidden="true"
//       >
//         <div className="modal-dialog">
//           <div className="modal-content">
//             <div className="modal-header">
//               <h5 className="modal-title" id="addTorrentModalLabel">
//                 Adding 1 Torrent
//               </h5>
//               <button
//                 type="button"
//                 className="btn-close"
//                 data-bs-dismiss="modal"
//                 aria-label="Close"
//               ></button>
//             </div>
//             <div className="modal-body">
//               <div>
//                 <input
//                   type="file"
//                   onChange={handleFileChange}
//                   className="form-control mb-3"
//                   accept=".torrent"
//                 />
//                 {/* <p>{file && "1 File, " + fileInfo.size}</p> */}
//                 <p>
//                   Peers: 0 | Seeds: 0{" "}
//                   <span className="badge bg-warning text-dark">
//                     Low peers and seeds
//                   </span>
//                 </p>
//               </div>

//               {/* <table className="table table-bordered">
//                 <thead>
//                   <tr>
//                     <th scope="col">
//                       <input type="checkbox" checked />
//                       Name
//                     </th>
//                     <th scope="col">Size</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   <tr>
//                     <td>
//                       <input type="checkbox" checked />
//                       CSDL (TH) ASSIGNMENT 1.pdf
//                     </td>
//                     <td>384 KB</td>
//                   </tr>
//                 </tbody>
//               </table> */}

//               <div className="mb-3">
//                 <label className="form-label">Download this torrent to:</label>
//                 <div className="input-group">
//                   <input
//                     type="text"
//                     className="form-control"
//                     value="C:\Users\Do Truong Khoa\Downloads"
//                     readonly
//                   />
//                   <button className="btn btn-outline-secondary" type="button">
//                     Change
//                   </button>
//                 </div>
//               </div>

//               {/* <div className="form-check">
//                 <input
//                   className="form-check-input"
//                   type="checkbox"
//                   id="startDownload"
//                   checked
//                 />
//                 <label className="form-check-label" for="startDownload">
//                   Start downloading when torrent is added
//                 </label>
//               </div>
//               <div className="form-check">
//                 <input
//                   className="form-check-input"
//                   type="checkbox"
//                   id="dontShowDialog"
//                 />
//                 <label className="form-check-label" for="dontShowDialog">
//                   Don’t show this dialog next time I add a torrent
//                 </label>
//               </div> */}
//             </div>

//             <div className="modal-footer">
//               <button
//                 type="button"
//                 className="btn btn-secondary"
//                 data-bs-dismiss="modal"
//               >
//                 Cancel
//               </button>
//               <button
//                 type="button"
//                 className="btn btn-primary"
//                 onClick={(e) => handleAddTorrent(e)}
//               >
//                 Add
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </>
//   );
// }
import { useRef } from "react";
// import { table } from "console";

export default function Home() {
  const [torrentFile, setTorrentFile] = useState(null);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  // const [downloading, setDownloading] = useState({}); // Object to hold downloading status for each file
  // const [downloadProgress, setDownloadProgress] = useState({});
  // const { user } = useContext(AuthContext);
  // const fileInputRef = useRef(null);
  const [value, setValue] = useState({
    'path_input': '',
    'path_output': ''
  })
  const [taskIds, setTaskIds] = useState([]); // Sử dụng mảng để lưu trữ taskId 
  const [taskStatuses, setTaskStatuses] = useState({}); // Sử dụng đối tượng để lưu trữ trạng thái của các task

  const checkThreadStatus = async (task_id) => { 
    try { 
      const response = await AxiosInstance.get(`/get-thread-status/${task_id}/`); 
      return response.data.status; 
    } catch (error) { 
      console.error('Failed to fetch thread status:', error); 
      return 'error'; // Trả về "error" nếu có lỗi 
      } 
  };

  const startCheckingStatus = (taskId) => { 
    const intervalId = setInterval(async () => { 
      const status = await checkThreadStatus(taskId); 
      setTaskStatuses(prevStatuses => ({ ...prevStatuses, [taskId]: status })); 
      if (status === 'completed') { 
        clearInterval(intervalId); 
      } 
    }, 5000); // Kiểm tra mỗi 5 giây 
  };

  const [seeds, setSeeds] = useState([])
  
  const handleFileChange = (event) => {
    if (torrentFile !== null) {
      setTorrentFile(null);
    } else {
      const selectedFile = event.target.files[0];
      setTorrentFile(selectedFile);
      setValue({...value, path_input: selectedFile.name})
      setError(null);
    }
  };

  const handleCancel = () => {
    setTorrentFile(null);
    setError(null);
    // if (fileInputRef.current) { fileInputRef.current.value = ''; }
  };



  const handleFileUpload = async () => {
    if (!torrentFile) {
      setError("No file selected.");
      return;
    }

    setError(null);
    setUploading(true);

    const formData = new FormData();
    formData.append("file", torrentFile);
    formData.append("command", "down");
    formData.append("path_output", value.path_output);
    try {
      const response = await AxiosInstance.post("/upload-torrent/", formData);
      setTaskIds([...taskIds, response.data.task_id]);
      startCheckingStatus(response.data.task_id);
      //setSeeds([...seeds, {name: getFileName(value.path_input), status: "downloading...", task_id: response.data.task_id}])
      // console.log("Download Successful:", response.data);
    } catch (error) {
      console.error("Download Failed:", error);
      setError("Download Failed: " + error.message);
    } finally {
      setUploading(false);
    }
  };
  const getFileName = (path) => { 
    return path.substring(path.lastIndexOf('\\') + 1); // Lấy phần sau ký tự `\` cuối cùng 
  };

  const handleCreateTorrent = async () => {
    setError(null);
    setUploading(true);
    const formData = new FormData();
    formData.append("command", "run");
    formData.append("path_input", value.path_input);
    formData.append("path_output", value.path_output);
    console.log(formData)
  
    try {
      const response = await AxiosInstance.post("/generate_torrent/", formData);
      setSeeds([...seeds, {name: getFileName(value.path_input), status: "seeding...", task_id: response.data.task_id}])
      console.log("Upload Successful:", response.data);
      // toast.success("Torrent created successfully!");
    } 
    catch (error) {
      console.error("Upload Failed:", error);
      setError(
        "Upload Failed: " + (error.response?.data?.message || error.message)
      );
      // toast.error("Failed to create torrent. Check your input and try again.");
    } 
    finally {
      setUploading(false);
    }
  };

  const handleStop = async (task_id) => {
    setError(null);
    setUploading(true);
    const formData = new FormData();
    formData.append("command", "stop");
    formData.append("task_id", task_id);
    console.log(formData)
  
    try {
      const response = await AxiosInstance.post("/generate_torrent/", formData);
      console.log("Stoped Successful:", response.data);
      // toast.success("Torrent created successfully!");
      setSeeds(prevSeeds => prevSeeds.filter(seed => seed.task_id !== task_id));
    } 
    catch (error) {
      console.error("Upload Failed:", error);
      setError(
        "Upload Failed: " + (error.response?.data?.message || error.message)
      );
      // toast.error("Failed to create torrent. Check your input and try again.");
    } 
    finally {
      setUploading(false);
    }
  }

  //   try {
  //     const response = await fetch(
  //       "http://127.0.0.1:8000/upload-torrent/",
  //       {
  //         method: "POST",
  //         headers: {
  //         },
  //         body: formData,
  //       }
  //     );

  //     if (!response.ok) {
  //       const errorData = await response.json();
  //       throw new Error(
  //         errorData.error || "An error occurred while uploading the file."
  //       );
  //     }

  //     const data = await response.json();
  //     const newFile = {
  //       id: Date.now(),
  //       name: file.name,
  //       torrentInfo: data.torrentInfo,
  //       fileContent: data.fileContent,
  //     };

  //     setTorrentFiles((prevFiles) => [...prevFiles, newFile]);
  //     toast.success("File uploaded successfully!");
  //   } catch (error) {
  //     setError(error.message);
  //   } finally {
  //     setUploading(false);
  //   }
  // };

  return (
    <>
      <div className="d-flex flex-column align-items-center justify-content-center mb-4 pt-2">
        <div className="w-100 rounded bg-white border shadow">
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
          <hr />
          <div>
          {seeds.length > 0 ? (
            <table className="table table-hover table-striped align-middle">
          <thead>
              <tr>
                  <th>Name</th>
                  <th>Status</th>
                  <th>User Action</th>
              </tr>
          </thead>
          <tbody>
          {seeds.map((d,i) => (
            <tr key={i}>
                <td style={{ width: 180, textTransform: 'uppercase', fontWeight: 500 }}>{d.name}</td>
                <td style={{ width: 170 }}>{d.status}</td>
                <td>
                    <button onClick={()=>handleStop(d.task_id)}  className="btn btn-sm btn-danger">stop</button>
                </td>
                
            </tr>

          ))}
          </tbody>
          </table>
          ):""}
          </div>
          <div>

          {taskIds.map(taskId => ( 
            <div key={taskId}> 
              <p>Checking status for task: {taskId}</p> 
                <table> 
                  <tbody> 
                    <tr> 
                      <td style={{ width: 170 }}>
                        {taskStatuses[taskId] === "completed" ? "Downloaded" : taskStatuses[taskId]}
                      </td> 
                    </tr> 
                  </tbody> 
                </table> 
               
            </div> 
          ))}

          </div>
          {uploading && (
            <>
            <div className="text-blue-500 font-semibold">Downloading...</div>
            <hr />
            </>
          )}
        </div>
      </div>
      
      {/* MODAL AddTorrent */}
      <div
        className="modal fade"
        id="addTorrentModal"
        tabIndex="-1"
        aria-labelledby="addTorrentModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="addTorrentModalLabel">
                Adding Torrent
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                onClick={handleCancel}
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
              </div>

              <div className="mb-3">
                <label className="form-label">Download this torrent to:</label>
                <div className="input-group">
                  <input
                    type="text"
                    value={value.path_output}
                    onChange={(e) => setValue({...value, path_output: e.target.value}) }
                    className="form-control"
                  />
                </div>
              </div>
            </div>

            <div className="modal-footer">
              {error && <div className="alert alert-danger">{error}</div>}
              <button
                type="button"
                className="btn btn-secondary"
                data-bs-dismiss="modal"
                onClick={handleCancel}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                {...(torrentFile ? { 'data-bs-dismiss': 'modal' } : {})}
                onClick={handleFileUpload}
              >
                Add
              </button>

            </div>
          </div>
        </div>
      </div>
      {/* MODAL CreateTorrent */}
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
                Create Torrent
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                onClick={handleCancel}
              ></button>
            </div>
            <div className="modal-body">
              {error && <div className="alert alert-danger">{error}</div>}
              <label className="form-label">Upload file from:</label>
              <div className="mb-3">
                <input
                  type="text"
                  value={value.path_input}
                  onChange={(e) => setValue({...value, path_input: e.target.value}) }
                  className="form-control mb-3"
                  // accept=".zip,.rar,.txt,.pdf,.docx,.xlsx,.png,.jpg,.jpeg,.mp3,.mp4,.avi,.mkv"
                  // ref={fileInputRef}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Download this torrent to:</label>
                <div className="input-group">
                  <input
                    type="text"
                    value={value.path_output}
                    onChange={(e) => setValue({...value, path_output: e.target.value}) }
                    className="form-control"
                  />
                </div>
              </div>
              {uploading && (
                <div className="text-center">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                  <p>Creating torrent...</p>
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-bs-dismiss="modal"
                onClick={handleCancel}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                data-bs-dismiss="modal"
                onClick={handleCreateTorrent}
              >
                Create Torrent
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

// <div className="flex flex-col items-center p-8 font-sans max-w-lg mx-auto border border-gray-300 rounded-lg shadow-lg">

//   <h1 className="text-3xl font-bold text-gray-800 mb-6">
//     Torrent File Downloader
//   </h1>
//   <input
//     type="file"
//     onChange={handleFileUpload}
//     className="mb-4 p-2 border border-gray-300 rounded w-full"
//   />

{
  /* {torrentFiles.map((file) => (
        <div key={file.id} className="mt-6 bg-gray-100 p-4 rounded-lg w-full">
          <h2 className="text-xl font-semibold mb-4">Uploaded File Info</h2>
          <p className="mb-2">
            <strong>File Name:</strong> {file.name}
          </p>
          <p className="mb-2">
            <strong>Tracker URL:</strong> {file.torrentInfo.trackerURL}
          </p>
          <p className="mb-2">
            <strong>File Length:</strong> {file.torrentInfo.length}
          </p>
          <p className="mb-2">
            <strong>Piece Length:</strong> {file.torrentInfo.pieceLength}
          </p>
          <p className="mb-2">
            <strong>Info Hash:</strong> {file.torrentInfo.infoHash}
          </p>

          <button
            onClick={() => handleDownload(file)}
            className="mt-4 p-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
            disabled={downloading[file.id]}
          >
            {downloading[file.id] ? "Downloading..." : "Download File"}
          </button>

          {downloading[file.id] && downloadProgress[file.id] && (
            <div className="mt-4 w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-blue-500 h-4 rounded-full"
                style={{ width: `${downloadProgress[file.id]}%` }}
              ></div>
            </div>
          )}
        </div>
      ))} */
}
//
// </div>
