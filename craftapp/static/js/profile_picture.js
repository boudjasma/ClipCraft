Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-drapzone", {
    maxFiles: 1,
    acceptedFiles: ".jpeg,.jpg,.png,.gif,.jfif",
    parallelUploads: 2,
    thumbnailHeight: 200,
    thumbnailWidth: 200,
    maxFilesize: 3,
    filesizeBase: 1000,
    thumbnail: function(file, dataUrl) {
      if (file.previewElement) {
        file.previewElement.classList.remove("dz-file-preview");
        var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
        for (var i = 0; i < images.length; i++) {
          var thumbnailElement = images[i];
          thumbnailElement.alt = file.name;
          thumbnailElement.src = dataUrl;
        }
        setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
      }
    }
  
  });
  