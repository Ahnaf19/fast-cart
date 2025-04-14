export const Wrapper = props => {
    return <>
      <header className="navbar sticky-top bg-dark flex-md-nowrap p-0 shadow" data-bs-theme="dark">
        <a className="navbar-brand col-md-3 col-lg-2 me-0 px-3 fs-6 text-white" href="#">Company name</a>
        <div style={{marginRight: "20px", textAlign: "right" }} className="navbar-nav ms-auto">
          <div className="nav-item text-nowrap">
            <a className="nav-link px-3" href="#">Sign out</a>
          </div>
        </div>
      </header>

      <div className="d-flex flex-column" style={{ height: '100vh', width: '100vw' }}>
        <div className="d-flex flex-grow-1">
          {/* Sidebar */}
          <div className="col-md-3 col-lg-2 p-0 bg-body-tertiary border-end">
            <div className="d-flex flex-column align-items-start p-3 bg-body-tertiary h-100">
              <ul className="nav nav-pills flex-column w-100">
                <li className="nav-item">
                  <a className="nav-link d-flex align-items-center gap-2" href="#">
                    Dashboard
                  </a>
                </li>
              </ul>
              <hr className="my-3 w-100" />
            </div>
          </div>

          {/* Main Content */}
          <main className="flex-grow-1 px-md-4">
            {props.children}
          </main>
        </div>
      </div>
    </>
}
