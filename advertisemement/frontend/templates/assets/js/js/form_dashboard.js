document.addEventListener('DOMContentLoaded', function () {
    const groups = [
        'number_of_memes_group',
        'type_of_memes_group',
        'type_of_movement_group',
        'type_of_subject_group',
        'type_of_emotion'
    ];

    let focusedGroupIndex = 0;

    function highlightFocusedGroup() {
        groups.forEach((groupId, index) => {
            const group = document.getElementById(groupId);
            if (group) {
                if (index === focusedGroupIndex) {
                    group.classList.add('focused');
                } else {
                    group.classList.remove('focused');
                }
            }
        });
    }

    function isTypeOfMemesBlocked() {
        const numberOfMemesRadio = document.querySelector('input[name="number_of_memes"]:checked');
        return numberOfMemesRadio && numberOfMemesRadio.value === '0';
    }

    function focusNextGroup() {
        do {
            focusedGroupIndex = (focusedGroupIndex + 1) % groups.length;
        } while (groups[focusedGroupIndex] === 'type_of_memes_group' && isTypeOfMemesBlocked());
        highlightFocusedGroup();
    }

    function focusPreviousGroup() {
        do {
            focusedGroupIndex = (focusedGroupIndex - 1 + groups.length) % groups.length;
        } while (groups[focusedGroupIndex] === 'type_of_memes_group' && isTypeOfMemesBlocked());
        highlightFocusedGroup();
    }

    function selectNextRadio() {
        const group = document.getElementById(groups[focusedGroupIndex]);
        const radios = group.querySelectorAll('input[type="radio"]');
        const checkedRadio = Array.from(radios).find(radio => radio.checked);
        const checkedIndex = Array.from(radios).indexOf(checkedRadio);
        radios[(checkedIndex + 1) % radios.length].click(); // Trigger click event
    }

    function selectPreviousRadio() {
        const group = document.getElementById(groups[focusedGroupIndex]);
        const radios = group.querySelectorAll('input[type="radio"]');
        const checkedRadio = Array.from(radios).find(radio => radio.checked);
        const checkedIndex = Array.from(radios).indexOf(checkedRadio);
        radios[(checkedIndex - 1 + radios.length) % radios.length].click(); // Trigger click event
    }

    function blockTypeOfMemes() {
        const numberOfMemesRadio = document.querySelector('input[name="number_of_memes"]:checked');
        const typeOfMemesRadios = document.querySelectorAll('input[name="type_of_memes"]');

        if (numberOfMemesRadio && numberOfMemesRadio.value === '0') {
            typeOfMemesRadios.forEach(radio => {
                radio.disabled = true;
                if (radio.value === '0') {
                    radio.checked = true;
                }
            });
        } else {
            typeOfMemesRadios.forEach(radio => {
                radio.disabled = false;
            });
        }
    }

    // Event listeners for number_of_memes and corresponding type_of_memes handling
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
    const postIdInput = document.querySelector('input[name="postid_input"]');
    const userIdInput = document.querySelector('input[name="userid_input"]');

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

    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            contentVideo.requestFullscreen().catch(err => {
                alert(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
            });
        } else {
            document.exitFullscreen();
        }
    }

    document.addEventListener('keydown', function (event) {
        if (event.ctrlKey || event.altKey || event.metaKey) return;

        const activeElement = document.activeElement;

        switch (event.key) {
            case 'ArrowUp':
                event.preventDefault();
                focusPreviousGroup();
                break;
            case 'ArrowDown':
                event.preventDefault();
                focusNextGroup();
                break;
            case 'ArrowLeft':
                event.preventDefault();
                selectPreviousRadio();
                break;
            case 'ArrowRight':
                event.preventDefault();
                selectNextRadio();
                break;
            case 'Enter':
                if (activeElement === postIdInput) {
                    event.preventDefault();
                    postIdInput.form.submit();
                } else if (activeElement === userIdInput) {
                    event.preventDefault();
                    userIdInput.form.submit();
                } else if (event.shiftKey) {
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
            case 'f':
                event.preventDefault();
                toggleFullscreen();
                break;
            default:
                break;
        }
    });

    highlightFocusedGroup(); // Initial highlight
    blockTypeOfMemes(); // Initial block
});
