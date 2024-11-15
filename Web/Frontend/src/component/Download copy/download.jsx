import { useState, useContext, useEffect } from "react";
// import AuthContext from "../../context/AuthContext"; // giả sử bạn đã thiết lập AuthContext
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AxiosInstance from "../AxiosInstance";

export default function Download() {
  return(
    <>
      heloooooooooooooooo
    </>
  )
}

// export default function Download() {
//   const [filesDownload, setfilesDownload] = useState([
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

//   useEffect(() => {
//     AxiosInstance.get(``)
//       .then((res) => setfilesDownload(res.data))
//       .catch((err) => console.log(err));
//   }, []);

//   const handleShow = (id) => {
//     setSelectedCard(selectedCard === id ? null : id);
//   };

//   const handleFileChange = (event) => {
//     if (event.target.files && event.target.files.length > 0) {
//       setFile(event.target.files[0]);
//       const file = event.target.files[0];
//       if (file) {
//         // Lưu trữ các thuộc tính tệp vào state
//         setFileInfo({
//           name: file.name,
//           size: (file.size / 1024).toFixed(2) + " KB", // Kích thước tính bằng MB
//           type: file.type,
//           lastModified: new Date(file.lastModified).toLocaleDateString(),
//         });
//       }
//     } else {
//       setFile(null);
//       toast.error("No file selected. Please choose a file to upload.");
//     }
//   };

//   const handleAddTorrent = () => {};
//   return (
//     <>
//       <ToastContainer />
//       <div className="d-flex justify-content-between align-items-center px-2 py-2 text-dark">
//         <div className="d-flex gap-2">
//           <button className="btn btn-outline-secondary d-flex align-items-center">
//             <i className="bi bi-grid-3x3-gap me-1"></i>
//             <i className="bi bi-chevron-down"></i>
//           </button>
//           <button className="btn btn-outline-secondary dropdown-toggle">
//             Show: All
//           </button>
//           <button className="btn btn-outline-secondary dropdown-toggle">
//             Sort: Most Recent
//           </button>
//         </div>
//         <div className="d-flex gap-2">
//           {/* <button
//             className="btn btn-outline-primary"
//             data-bs-toggle="modal"
//             data-bs-target="#createTorrentModal"
//           >
//             Create torrent <i className="bi bi-plus"></i>
//           </button> */}
//           <button
//             className="btn btn-outline-secondary"
//             data-bs-toggle="modal"
//             data-bs-target="#addTorrentModal"
//           >
//             Add torrent <i className="bi bi-plus"></i>
//           </button>
//         </div>
//       </div>

//       <div className="d-flex flex-column align-items-center justify-content-center px-1 my-3">
//         <div className="w-100 rounded-4 bg-white border shadow">
//           {filesDownload.map((d) => (
//             <div key={d.id} className="my-3 border-bottom">
//               <div className="d-flex align-items-center p-3">
//                 <div className="flex-shrink-0 me-3">
//                   <i
//                     className="bi bi-download"
//                     style={{ fontSize: "1.5rem" }}
//                   ></i>
//                 </div>
//                 <div className="flex-grow-1">
//                   <h5 className="mb-0">{d.name}</h5>
//                   <div className="d-flex align-items-center mt-1">
//                     <span className="badge bg-success me-2">Dowloading</span>
//                     <span className="text-muted">0 B/s</span>
//                   </div>
//                 </div>
//                 <div className="d-flex gap-2">
//                   <button className="btn btn-outline-dark btn-sm">
//                     <i className="bi bi-share"></i>
//                   </button>
//                   <button className="btn btn-outline-dark btn-sm">
//                     <i className="bi bi-folder"></i>
//                   </button>
//                   <button className="btn btn-outline-dark btn-sm">
//                     <i className="bi bi-trash"></i>
//                   </button>
//                   <button
//                     className="btn btn-outline-dark btn-sm"
//                     onClick={() => handleShow(d.id)}
//                   >
//                     <i className="bi bi-info-circle"></i>
//                   </button>
//                 </div>
//               </div>
//               {selectedCard === d.id && (
//                 <div className="bg-light p-3 rounded-bottom">
//                   <div className="d-flex justify-content-between">
//                     <div>
//                       <strong>Date Added</strong>
//                       <div>{new Date(d.dateAdd).toLocaleDateString()}</div>
//                       <strong>Total Files</strong>
//                       <div>{d.totalFile} File</div>
//                       <strong>Total Size</strong>
//                       <div>{d.totalSize}</div>
//                     </div>
//                     <div className="d-flex flex-column align-items-center">
//                       <strong>Torrent files</strong>
//                       <span className="text-muted">{d.name}</span>
//                     </div>
//                   </div>
//                 </div>
//               )}
//             </div>
//           ))}
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
//                 class="btn-close"
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
//                 <p>{file && "1 File, " + fileInfo.size}</p>
//                 <p>
//                   Peers: 0 | Seeds: 0{" "}
//                   <span className="badge bg-warning text-dark">
//                     Low peers and seeds
//                   </span>
//                 </p>
//               </div>

//               {/* <table class="table table-bordered">
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

//               <div class="mb-3">
//                 <label class="form-label">Download this torrent to:</label>
//                 <div class="input-group">
//                   <input
//                     type="text"
//                     class="form-control"
//                     value="C:\Users\Do Truong Khoa\Downloads"
//                     readonly
//                   />
//                   <button class="btn btn-outline-secondary" type="button">
//                     Change
//                   </button>
//                 </div>
//               </div>

//               {/* <div class="form-check">
//                 <input
//                   class="form-check-input"
//                   type="checkbox"
//                   id="startDownload"
//                   checked
//                 />
//                 <label class="form-check-label" for="startDownload">
//                   Start downloading when torrent is added
//                 </label>
//               </div>
//               <div class="form-check">
//                 <input
//                   class="form-check-input"
//                   type="checkbox"
//                   id="dontShowDialog"
//                 />
//                 <label class="form-check-label" for="dontShowDialog">
//                   Don’t show this dialog next time I add a torrent
//                 </label>
//               </div> */}
//             </div>

//             <div class="modal-footer">
//               <button
//                 type="button"
//                 class="btn btn-secondary"
//                 data-bs-dismiss="modal"
//               >
//                 Cancel
//               </button>
//               <button
//                 type="button"
//                 class="btn btn-primary"
//                 onClick={() => handleAddTorrent()}
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
