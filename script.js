window.addEventListener("load", () => {
  setTimeout(() => {
    document.querySelector(".logo-intro").style.display = "none";
    document.querySelector(".container").classList.remove("hidden");
  }, 2000);
});

const imageUpload = document.getElementById("imageUpload");
const previewImage = document.getElementById("previewImage");
const captionOutput = document.getElementById("captionOutput");

imageUpload.addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (file) {
    previewImage.src = URL.createObjectURL(file);
    previewImage.classList.remove("hidden"); // ✅ THIS FIXED IT
    previewImage.classList.add("show");
    captionOutput.textContent = "⏳ Generating caption...";

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/caption", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (data.caption) {
        captionOutput.textContent = data.caption;
      } else {
        captionOutput.textContent = "❌ Failed to get caption.";
        console.error("Backend error:", data);
      }

    } catch (error) {
      captionOutput.textContent = "❌ Error connecting to backend.";
      console.error(error);
    }
  }
});

document.getElementById("playBtn").addEventListener("click", () => {
  const utterance = new SpeechSynthesisUtterance(captionOutput.textContent);
  speechSynthesis.speak(utterance);
});
