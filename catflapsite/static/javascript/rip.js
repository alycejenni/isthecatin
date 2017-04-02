function refreshContent(animalb64){
    var animal = JSON.parse(window.atob(animalb64))[0].fields;

    var animalType;
    if (animal.creature_type === ""){
        animalType = "mysterious creature"
    }
    else {
        animalType = animal.creature_type;
    }

    var animalName;
    if (animal.creature_name === ""){
        animalName = "little " + animalType
    }
    else {
        animalName = animal.creature_name + " the " + animalType;
    }

    var obitTitle;
    var obitDesc;
    var obitHeader = $('#obit_header');
    obitHeader.attr("class", "h1");
    if (animal.doa){
        obitHeader.addClass("ded");
        obitTitle = "alas, poor " + animalName;
        obitDesc = "you were dead before you reached us";
    }
    else if (animal.known_deceased){
        obitHeader.addClass("ded");
        obitTitle = "sorry, " + animalName;
        obitDesc = "we could not save you from the fluffy menace";
    }
    else {
        obitHeader.addClass("notded");
        obitTitle = "well done, " + animalName;
        obitDesc = "you actually left the house alive, though we apologise for the severe mental and physical trauma inflicted on you by the fluffy menace"
    }

    obitHeader.text(obitTitle);
    $('#obit_desc').text(obitDesc);

    $('#catflappicture').attr("src", animal.url);

    $('#critterpicture').attr("src", animal.additional_image);

    $('#guiltycat').attr("src", animal.guilty_cat);


}