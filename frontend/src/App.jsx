import { useState, useEffect } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState("");

  async function submitJob() {

    const response = await fetch(
      "http://127.0.0.1:8000/api/jobs",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          name,
        }),
      }
    );

    const data = await response.json();

    setJobId(data.job_id);
    setStatus(data.status);
  }

  useEffect(() => {
  if (!jobId) return;

  const interval = setInterval(async () => {
    const response = await fetch(
      `http://127.0.0.1:8000/api/jobs/${jobId}`
    );

    const data = await response.json();

    setStatus(data.status);

    if (data.status === "completed") {
      clearInterval(interval);
    }
  }, 1000);

  return () => clearInterval(interval);

}, [jobId]);
  return (
    <>
    <div className="container">
      <h1>Welcome Email Queue</h1>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <button onClick={submitJob}>
        Send Welcome Email
      </button>
      {jobId && (
        <>
          <h3>Job ID</h3>
          <p>{jobId}</p>

          <h3>Status</h3>
          <p>{status}</p>
        </>
      )}
      </div>
    </>
  );
}

export default App;