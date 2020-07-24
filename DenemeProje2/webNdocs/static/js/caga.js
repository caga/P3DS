// function ilk(){
//     document.getElementById("demo").innerHTML="Paragraf değiştirildi";
// }
document.createElement("ustluk")
document.createElement("ustmenu")
document.createElement("yanmenu")
document.createElement("icerik")
document.createElement("altlik")
document.createElement("arkaresim")

var toggler=document.getElementsByClassName("klasor");
var i;
for (i=0; i<toggler.length;i++){
    toggler[i].addEventListener("click",function(){
        this.parentElement.querySelector(".tree").classList.toggle("active");
        this.classList.toggle("klasor-down");
    });
}
