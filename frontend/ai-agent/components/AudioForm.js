"use client"; // Add this at the very top of the file

import { useState } from 'react';

export default function AudioForm() {
  const [audioFile, setAudioFile] = useState(null);
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!audioFile) {
      alert('Please upload an audio file!');
      return;
    }

    const formData = new FormData();
    formData.append('audio', audioFile);

    setIsLoading(true);
    setResponse('');

    try {
      const res = await fetch('/api/speak', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        setResponse(`Error: ${errorData.message}`);
        return;
      }

      const data = await res.json();
      setResponse(`Response: ${data.message}`);
    } catch (error) {
      console.error(error);
      setResponse('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setAudioFile(e.target.files[0])}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Submitting...' : 'Submit'}
        </button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}
