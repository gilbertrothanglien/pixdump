document.addEventListener('DOMContentLoaded', () => {
	const fileInput = document.getElementById('upload');
	fileInput.onchange = () => {
	  const selectedFile = fileInput.files[0];
	  document.getElementById('upload-text').innerHTML = selectedFile['name']
	  document.getElementById('profile_picture_name').value = selectedFile['name']
	}
})