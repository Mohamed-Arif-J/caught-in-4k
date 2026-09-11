import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

export default function App() {
  const webcamRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('Ready CAPS NUM');
  const [result, setResult] = useState(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: 'user',
  };

  const captureAndGenerate = useCallback(async () => {
    if (!webcamRef.current) return;
    const screenshot = webcamRef.current.getScreenshot();
    if (!screenshot) {
      alert('Camera frame buffer capture failed.');
      return;
    }

    setLoading(true);
    setStatusMsg('Capturing optical buffer & running neural models...');

    try {
      const fetchRes = await fetch(screenshot);
      const blob = await fetchRes.blob();

      const formData = new FormData();
      formData.append('file', blob, 'user_capture.jpg');

      // FIX: Explicitly target FastAPI on Port 8000 to avoid Vite 404
      const response = await axios.post('http://127.0.0.1:8000/generate-caught-meme', formData, {
        responseType: 'blob',
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const memeBlobUrl = URL.createObjectURL(response.data);

      const decodeHeader = (val, fallback) => {
        try {
          return val ? decodeURIComponent(val) : fallback;
        } catch {
          return val || fallback;
        }
      };

      const memeName = decodeHeader(response.headers['x-meme-name'], 'Matched Template');
      const userVibe = decodeHeader(response.headers['x-user-reaction'], 'Analyzed');
      const topText = decodeHeader(response.headers['x-top-text'], '');
      const bottomText = decodeHeader(response.headers['x-bottom-text'], '');

      setResult({
        capturedImage: screenshot,
        memeUrl: memeBlobUrl,
        memeName,
        userVibe,
        topText,
        bottomText,
      });
      setStatusMsg('Ready CAPS NUM');
    } catch (err) {
      console.error(err);
      setStatusMsg('Error: Check if server.py is running on port 8000');
      alert('Connection Failed: Make sure server.py is running on port 8000.');
    } finally {
      setLoading(false);
    }
  }, [webcamRef]);

  const resetSession = () => {
    if (result?.memeUrl) {
      URL.revokeObjectURL(result.memeUrl);
    }
    setResult(null);
    setStatusMsg('Ready CAPS NUM');
  };

  return (
    <div style={styles.desktop}>
      {/* Authentic Windows 95/98 Window */}
      <div style={styles.window}>
        
        {/* Title Bar */}
        <div style={styles.titleBar}>
          <div style={styles.titleText}>
            <span style={styles.titleIcon}>📷</span>
            Optical Sensor - [Caught in 4K Parody Subsystem]
          </div>
          <div style={styles.windowControls}>
            <button style={styles.titleBtn}>_</button>
            <button style={styles.titleBtn}>□</button>
            <button style={styles.titleBtn} onClick={() => window.close()}>✕</button>
          </div>
        </div>

        {/* Menu Bar */}
        <div style={styles.menuBar}>
          <span style={styles.menuItem}><u>F</u>ile</span>
          <span style={styles.menuItem}><u>E</u>dit</span>
          <span style={styles.menuItem}><u>V</u>iew</span>
          <span style={styles.menuItem}><u>H</u>elp</span>
        </div>

        {/* Window Content */}
        <div style={styles.windowBody}>
          {!result ? (
            /* Mode 1: Live Sensor View */
            <div style={styles.viewSection}>
              <div style={styles.sunkenViewport}>
                <Webcam
                  audio={false}
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  videoConstraints={videoConstraints}
                  style={styles.mediaElement}
                />
              </div>

              {/* Action Buttons */}
              <div style={styles.controlRow}>
                <button
                  onClick={captureAndGenerate}
                  disabled={loading}
                  style={styles.beveledBtn}
                >
                  {loading ? 'Processing...' : 'Capture Reaction (F5)'}
                </button>
              </div>

              {/* Optical Telemetry Group Box */}
              <fieldset style={styles.groupBox}>
                <legend style={styles.groupLegend}>Optical Telemetry</legend>
                <div style={styles.telemetryGrid}>
                  <div>OPTICAL STATUS: <span style={{ color: '#008000', fontWeight: 'bold' }}>ONLINE (CALIBRATED)</span></div>
                  <div>DEVICE: <span style={{ fontWeight: 'bold' }}>RTX 4050 ACCELERATED</span></div>
                  <div>DRIVER: <span style={{ fontWeight: 'bold' }}>VFW32 / LOCALHOST:8000</span></div>
                  <div>NEURAL PIPELINE: <span style={{ fontWeight: 'bold' }}>MOONDREAM2 + QWEN</span></div>
                </div>
              </fieldset>
            </div>
          ) : (
            /* Mode 2: Vertical Stack (Input Top -> Output Bottom -> Diagnostics Bottom) */
            <div style={styles.verticalResultContainer}>
              
              {/* 1. Live Input Frame */}
              <div style={styles.resultItem}>
                <div style={styles.subHeader}>1. Optical Sensor Buffer [Live Input]</div>
                <div style={styles.sunkenViewport}>
                  <img
                    src={result.capturedImage}
                    alt="Webcam Input"
                    style={styles.mediaElement}
                  />
                </div>
              </div>

              {/* 2. Output Meme Frame */}
              <div style={styles.resultItem}>
                <div style={styles.subHeader}>2. Generated Parody [AI Burned Output]</div>
                <div style={styles.sunkenViewport}>
                  <img
                    src={result.memeUrl}
                    alt={result.memeName}
                    style={styles.mediaElement}
                  />
                </div>
              </div>

              {/* Action Controls */}
              <div style={styles.controlRow}>
                <a
                  href={result.memeUrl}
                  download={`caught_in_4k_${Date.now()}.jpg`}
                  style={styles.beveledBtnLink}
                >
                  Save Image...
                </a>
                <button onClick={resetSession} style={styles.beveledBtn}>
                  Retake Face...
                </button>
              </div>

              {/* Telemetry Diagnostics at the Very Bottom */}
              <fieldset style={styles.groupBox}>
                <legend style={styles.groupLegend}>Cognitive Evaluation Report</legend>
                <div style={styles.telemetryGrid}>
                  <div>DETECTED VIBE: <span style={{ color: '#000080', fontWeight: 'bold' }}>"{result.userVibe}"</span></div>
                  <div>PARODY TEMPLATE: <span style={{ color: '#000080', fontWeight: 'bold' }}>{result.memeName}</span></div>
                </div>
              </fieldset>

            </div>
          )}
        </div>

        {/* Windows 95/98 Status Bar */}
        <div style={styles.statusBar}>
          <div style={styles.statusFieldLeft}>{statusMsg}</div>
          <div style={styles.statusFieldRight}>VFW32</div>
          <div style={styles.statusFieldRight}>PORT: 8000</div>
        </div>

      </div>
    </div>
  );
}

// Windows 95 / RAGEWARE 98 Design System
const styles = {
  desktop: {
    minHeight: '100vh',
    backgroundColor: '#008080', // Exact Windows 98 Teal
    backgroundImage: 'radial-gradient(#006666 15%, transparent 16%)',
    backgroundSize: '4px 4px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
    padding: '20px 10px',
    boxSizing: 'border-box',
    fontFamily: '"MS Sans Serif", Tahoma, Arial, sans-serif',
  },
  window: {
    width: '100%',
    maxWidth: '780px',
    backgroundColor: '#c0c0c0',
    borderTop: '2px solid #ffffff',
    borderLeft: '2px solid #ffffff',
    borderRight: '2px solid #000000',
    borderBottom: '2px solid #000000',
    boxShadow: '2px 2px 0px rgba(0,0,0,0.5)',
    display: 'flex',
    flexDirection: 'column',
    boxSizing: 'border-box',
  },
  titleBar: {
    height: '20px',
    background: 'linear-gradient(90deg, #000080 0%, #1084d0 100%)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '2px 3px',
    userSelect: 'none',
  },
  titleText: {
    color: '#ffffff',
    fontSize: '11px',
    fontWeight: 'bold',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    letterSpacing: '0.3px',
  },
  titleIcon: {
    fontSize: '12px',
  },
  windowControls: {
    display: 'flex',
    gap: '2px',
  },
  titleBtn: {
    width: '16px',
    height: '14px',
    backgroundColor: '#c0c0c0',
    borderTop: '1px solid #ffffff',
    borderLeft: '1px solid #ffffff',
    borderRight: '1px solid #000000',
    borderBottom: '1px solid #000000',
    fontSize: '9px',
    fontWeight: 'bold',
    lineHeight: 1,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer',
    padding: 0,
    outline: 'none',
  },
  menuBar: {
    display: 'flex',
    gap: '12px',
    padding: '2px 6px',
    borderBottom: '1px solid #808080',
    fontSize: '11px',
    color: '#000000',
    backgroundColor: '#c0c0c0',
  },
  menuItem: {
    cursor: 'pointer',
  },
  windowBody: {
    padding: '10px',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    backgroundColor: '#c0c0c0',
  },
  viewSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  verticalResultContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  resultItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  subHeader: {
    fontSize: '11px',
    fontWeight: 'bold',
    color: '#000000',
  },
  sunkenViewport: {
    backgroundColor: '#000000',
    borderTop: '2px solid #808080',
    borderLeft: '2px solid #808080',
    borderRight: '2px solid #ffffff',
    borderBottom: '2px solid #ffffff',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  mediaElement: {
    width: '100%',
    height: 'auto',
    maxHeight: '420px',
    objectFit: 'contain',
    display: 'block',
  },
  controlRow: {
    display: 'flex',
    justifyContent: 'center',
    gap: '10px',
    margin: '4px 0',
  },
  beveledBtn: {
    fontFamily: '"MS Sans Serif", Tahoma, Arial, sans-serif',
    fontSize: '11px',
    fontWeight: 'bold',
    padding: '5px 22px',
    backgroundColor: '#c0c0c0',
    borderTop: '2px solid #ffffff',
    borderLeft: '2px solid #ffffff',
    borderRight: '2px solid #000000',
    borderBottom: '2px solid #000000',
    color: '#000000',
    cursor: 'pointer',
    outline: 'none',
  },
  beveledBtnLink: {
    fontFamily: '"MS Sans Serif", Tahoma, Arial, sans-serif',
    fontSize: '11px',
    fontWeight: 'bold',
    padding: '5px 22px',
    backgroundColor: '#c0c0c0',
    borderTop: '2px solid #ffffff',
    borderLeft: '2px solid #ffffff',
    borderRight: '2px solid #000000',
    borderBottom: '2px solid #000000',
    color: '#000000',
    textDecoration: 'none',
    display: 'inline-block',
  },
  groupBox: {
    borderTop: '1px solid #ffffff',
    borderLeft: '1px solid #ffffff',
    borderRight: '1px solid #808080',
    borderBottom: '1px solid #808080',
    boxShadow: '-1px -1px 0px #808080 inset, 1px 1px 0px #ffffff inset',
    padding: '8px 12px',
    margin: '4px 0 0 0',
  },
  groupLegend: {
    fontSize: '11px',
    fontWeight: 'bold',
    color: '#000000',
    padding: '0 4px',
  },
  telemetryGrid: {
    fontSize: '11px',
    color: '#000000',
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '6px',
    fontFamily: '"Lucida Console", "Courier New", monospace',
  },
  statusBar: {
    height: '22px',
    display: 'flex',
    gap: '4px',
    padding: '2px 4px',
    borderTop: '1px solid #808080',
    fontSize: '11px',
    backgroundColor: '#c0c0c0',
    boxSizing: 'border-box',
  },
  statusFieldLeft: {
    flex: 1,
    borderTop: '1px solid #808080',
    borderLeft: '1px solid #808080',
    borderRight: '1px solid #ffffff',
    borderBottom: '1px solid #ffffff',
    padding: '1px 6px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    color: '#000000',
  },
  statusFieldRight: {
    width: '100px',
    borderTop: '1px solid #808080',
    borderLeft: '1px solid #808080',
    borderRight: '1px solid #ffffff',
    borderBottom: '1px solid #ffffff',
    padding: '1px 6px',
    textAlign: 'center',
    color: '#000000',
  },
};