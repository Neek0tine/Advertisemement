document.addEventListener('DOMContentLoaded', function () {
    const numMemes = document.querySelectorAll('input[name="number_of_memes"]');
    const none = document.getElementById('typeNone');
    const textual = document.getElementById('typeTextual');
    const visual = document.getElementById('typeVisual');
    const auditory = document.getElementById('typeAuditory');
    const textualAuditory = document.getElementById('typeTextualAuditory');
    const textualVisual = document.getElementById('typeTextualVisual');
    const visualAuditory = document.getElementById('typeVisualAuditory');
    const textualVisualAuditory = document.getElementById('typeTextualVisualAuditory');
    
    
    numMemes.forEach((radio) => {
        radio.addEventListener('change', function () {
            if (this.value === '0') {
                none.checked = true;
                textual.disabled = true;
                visual.disabled = true;
                auditory.disabled = true;
                textualAuditory.disabled = true;
                textualVisual.disabled = true;
                visualAuditory.disabled = true;
                textualVisualAuditory.disabled = true;
            } else {
                none.disabled = true;
                none.checked = false;
                textual.disabled = false;
                visual.disabled = false;
                auditory.disabled = false;
                textualAuditory.disabled = false;
                textualVisual.disabled = false;
                visualAuditory.disabled = false;
                textualVisualAuditory.disabled = false;
            }
        });
    });
});