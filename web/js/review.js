function predictReview() {

    const encodedURI = encodeURI("http://127.0.0.1:5500/predict_review?review=" + document.getElementById("review").value)
    fetch(encodedURI)
        .then(response => response.json())
        .then(data => {
            let reviewId = "#review"
            const reviewText = $(reviewId).val();
            setCardReview(reviewText, data["prediction"])
            $(reviewId).val('')
            // document.getElementById("prediction").innerText = data["prediction"]
        });
}

function setCardBorderColor(color){
    $("#review" + count).attr('style', 'border-color:' + color + ' !important');
}

function setCorrectSpan(statusReview){

    let bodySpan = getCorrectBodySpanAndColor(statusReview)[0]
    let color = getCorrectBodySpanAndColor(statusReview)[1]

    return "<span class='material-icons' style='color:" + color + "'>" + bodySpan + "</span>"
}

function getCorrectBodySpanAndColor(statusReview){
    let bodySpan
    let color
    if (statusReview === "Good review"){
        bodySpan = "thumb_up"
        color = "green"
    } else {
        bodySpan = "thumb_down"
        color = "red"
    }

    return [bodySpan, color]
}

let count = 1

function setCardReview(reviewText, statusReview){
    $("#container-reviews").prepend(
        "<div class='card' id='review" + count + "' >" +
        "<div class='card-body'>" +
        "<h5 class='card-title'> Review " + count +  "</h5>" +
        "<h5 class='card-text'>" + reviewText + "</h5>" +
        setCorrectSpan(statusReview) +
        "</div>" +
        "</div>"
    )
    setCardBorderColor(getCorrectBodySpanAndColor(statusReview)[1])
    count = count + 1
}