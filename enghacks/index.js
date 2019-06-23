var mainText = document.getElementById("mainText")
var submitBtn = document.getElementById("submitBtn")

function submitClick() {
    window.alert("HELLOO");
    var database = firebase.database();
    firebaseRef.child("Text").set("Some Value");
}