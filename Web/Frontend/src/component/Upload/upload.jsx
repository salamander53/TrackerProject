import { useState } from "react";

export default function Upload() {
  const [fileUpload, setFileUpload] = useState([
    {
      id: 1,
      name: "file 1",
      dateAdd: Date.now(),
      totalFile: 2,
      totalSize: 100 + "mb",
    },
    {
      id: 2,
      name: "file 2",
      dateAdd: Date.now(),
      totalFile: 2,
      totalSize: 100 + "mb",
    },
  ]);

  const [selectedCard, setSelectedCard] = useState(null);

  const handleShow = (id) => {
    setSelectedCard(selectedCard === id ? null : id);
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center px-2 py-2  text-dark">
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
          <button className="btn btn-outline-secondary">
            Create torrent <i className="bi bi-plus"></i>
          </button>
          <button className="btn btn-primary">
            Add torrent <i className="bi bi-plus"></i>
          </button>
        </div>
      </div>

      <div className="d-flex flex-column align-items-center justify-content-center px-1 my-3">
        <div className="w-100 rounded-4 bg-white border shadow">
          {fileUpload.map((d) => (
            <div key={d.id} className="my-3 border-bottom">
              <div className="d-flex align-items-center p-3">
                <div className="flex-shrink-0 me-3">
                  <i
                    className="bi bi-download"
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
                      <div className="text-left">
                        <div className="mb-2">
                          <strong>Date Added</strong>
                          <div>{new Date(d.dateAdd).toLocaleDateString()}</div>
                        </div>
                        <div className="mb-2">
                          <strong>Total Files</strong>
                          <div>{d.totalFile} File</div>
                        </div>
                        <div>
                          <strong>Total Size</strong>
                          <div>{d.totalSize}</div>
                        </div>
                      </div>
                    </div>
                    <div className="d-flex flex-column align-items-center justify-content-center">
                      <span>
                        <strong>Torrent files</strong>
                      </span>
                      <span className="text-muted">{d.name}</span>
                      <span className="text-muted">Played</span>
                      <span className="text-muted">{d.totalSize}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
