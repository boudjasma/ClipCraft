
const myDropzone= new Dropzone('#my-dropzone',{
    url:'',
    maxFiles:1,
    acceptedFiles:'.jpg',
    maxFilesize: 2,  // Taille maximale du fichier en Mo
    acceptedFiles: "image/*",  // Types de fichiers acceptés (ici, uniquement des images)
    dictDefaultMessage: "Cliquez ici ou faites glisser une image pour changer votre photo de profil",
    // Gestionnaire d'événements Dropzone.js
    init: function() {
      this.on("complete", function(file) {
        // Réexécutez la page pour afficher la nouvelle image de profil après l'envoi réussi
        location.reload();
      });
    }
})