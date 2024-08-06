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
    const nextButton = document.querySelector('button[name="next"]');
    const previousButton = document.querySelector('button[name="previous"]');
    const contentVideo = document.getElementById('contentVideo');
    
    numMemes.forEach((radio) => {
        radio.addEventListener('change', function () {
            handleNumMemesChange(this.value);
        });
    });

    function handleNumMemesChange(value) {
        if (value === '0') {
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
    }

    document.addEventListener('keydown', function (event) {
        if (event.ctrlKey || event.altKey || event.metaKey) {
            return; // Ignore key combinations with Ctrl, Alt, Meta, or Shift
        }

        switch (event.key) {
            case '`':
                document.getElementById('zeroMeme').checked = true;
                handleNumMemesChange('0');
                break;
            case '1':
                document.getElementById('oneMeme').checked = true;
                handleNumMemesChange('1');
                break;
            case '2':
                document.getElementById('twoMeme').checked = true;
                handleNumMemesChange('2');
                break;
            case '3':
                document.getElementById('threeMeme').checked = true;
                handleNumMemesChange('3');
                break;
            case '4':
                document.getElementById('fourMeme').checked = true;
                handleNumMemesChange('4');
                break;
            case '5':
                document.getElementById('fiveMeme').checked = true;
                handleNumMemesChange('5');
                break;
            case '6':
                document.getElementById('moreThanFiveMeme').checked = true;
                handleNumMemesChange('6');
                break;


            case 'q':
                if (!textual.disabled) document.getElementById('typeTextual').checked = true;
                break;
            case 'w':
                if (!visual.disabled) document.getElementById('typeVisual').checked = true;
                break;
            case 'e':
                if (!auditory.disabled) document.getElementById('typeAuditory').checked = true;
                break;
            case 'a':
                if (!textualVisual.disabled) document.getElementById('typeTextualVisual').checked = true;
                break;
            case 's':
                if (!visualAuditory.disabled) document.getElementById('typeVisualAuditory').checked = true;
                break;
            case 'd':
                if (!textualAuditory.disabled) document.getElementById('typeTextualAuditory').checked = true;
                break;
            case 'f':
                if (!textualVisualAuditory.disabled) document.getElementById('typeTextualVisualAuditory').checked = true;
                break;


            case 'i':
                document.getElementById('noneMovement').checked = true;
                break;
            case 'o':
                document.getElementById('physicalMovement').checked = true;
                break;
            case 'p':
                document.getElementById('causalMovement').checked = true;
                break;
            case '[':
                document.getElementById('emotionalMovement').checked = true;
                break;


            case 'j':
                document.getElementById('physicalCausalMovement').checked = true;
                break;
            case 'k':
                document.getElementById('physicalEmotionalMovement').checked = true;
                break;
            case 'l':
                document.getElementById('physicalCausalEmotionalMovement').checked = true;
                break;


            case 'n':
                document.getElementById('subjectCharacter').checked = true;
                break;
            case 'm':
                document.getElementById('subjectObject').checked = true;
                break;
            case ',':
                document.getElementById('subjectCreature').checked = true;
                break;
            case '.':
                document.getElementById('subjectScene').checked = true;
                break;


            case 'z':
                document.getElementById('positiveEmotion').checked = true;
                break;
            case 'x':
                document.getElementById('neutralEmotion').checked = true;
                break;
            case 'c':
                document.getElementById('negativeEmotion').checked = true;
                break;


            case 'Enter':
                if (event.shiftKey) {
                    event.preventDefault();
                    previousButton.click();
                } else {
                    event.preventDefault();
                    nextButton.click();
                }
                break;
            
            case ' ':
                event.preventDefault();
                if (event.shiftKey) {
                    if (contentVideo) {
                        contentVideo.muted = !contentVideo.muted;
                    }
                } else if (event.ctrlKey) {
                    if (contentVideo) {
                        contentVideo.currentTime = 0;
                    }
                } else {
                    if (contentVideo) {
                        if (contentVideo.paused) {
                            contentVideo.play();
                        } else {
                            contentVideo.pause();
                        }
                    }
                }
                break;
            default:
                break;
        }
    });
});
