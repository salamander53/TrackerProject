export default function Download() {
  return (
    <>
      <div
        className="d-flex flex-column align-items-center justify-content-center px-4 my-5"
        // style={{ width: "1200px" }}
      >
        <div
          className="w-100 rounded-4 bg-white border shadow"
          style={{ minHeight: "300px" }}
        >
          <div className="d-flex justify-content-end align-items-center border-bottom">
            <div className="flex-grow-1 text-center my-3">
              <h5>Download</h5>
            </div>
            {/* <div className="mb-2 me-3">
              <i className="bi bi-people" style={{ fontSize: "1.9rem" }}></i>
            </div> */}
            <div className="d-flex flex-grow-1 align-items-center mx-3">
              {/* <Search
                onSearchChange={handleSearchChange}
                searchData={printer}
              /> */}
            </div>
            <button className="btn btn-success me-5 "> + Add File </button>
          </div>

          <div className="m-3">
            <table
              className="table table-hover table-striped text-center table-bordered mt-3 w-100"
              // style={{ width: "100%" }}
            >
              <thead>
                <tr>
                  <th>Mã máy in</th>
                  <th>Cơ sở</th>
                  <th>Tòa</th>
                  <th>Tầng-Phòng</th>
                  <th>Trạng thái</th>
                  <th>Cài đặt</th>
                </tr>
              </thead>
              <tbody>
                {/* {printer.map((d, i) => (
                  <tr key={i}>
                    <td style={{ width: 170 }}>{d.id}</td>
                    <td style={{ width: 170 }}>{d.campus}</td>
                    <td style={{ width: 170 }}>{d.building}</td>
                    <td style={{ width: 170 }}>{d.room}</td>
                    <td style={{ width: 170 }}>{d.status}</td>
                    <td style={{ width: 170 }}></td>
                  </tr>
                ))} */}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}
