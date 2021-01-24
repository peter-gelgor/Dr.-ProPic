

const fileUpload = document.getElementById("submit");
var file;
fileUpload.onclick = function (){
    file = document.getElementById("input").files[0];
    readImage(file);
}


function readImage(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        $.ajax({
            url: "https://eastus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/5d223f62-13e1-428b-a83f-4708a1e2cafe/classify/iterations/Iteration4/image",
            data: reader.result,
            processData: false,
            contentType: "application/octet-stream",
            headers: {
                'Prediction-key': '2d36364a0c854a8b8a204b798568dda5'
            },
            type: 'POST',
            success: function(response) {
                var result = response["Predictions"];

                alert(result);
            },
            error: function(error) {
                alert('error: ' + error);
            }
        });
    }
    reader.readAsArrayBuffer(file);
}
