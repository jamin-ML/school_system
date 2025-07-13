document.addEventListener('DOMContentLoaded', function() {
    // Video preview modal functionality
    const previewButtons = document.querySelectorAll('.preview-btn');
    
    previewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const videoUrl = this.getAttribute('data-video-url');
            openVideoModal(videoUrl);
        });
    });
    
    function openVideoModal(videoUrl) {
        // Create modal elements
        const modal = document.createElement('div');
        modal.className = 'video-modal';
        
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        
        const video = document.createElement('video');
        video.src = videoUrl;
        video.controls = true;
        
        const closeBtn = document.createElement('span');
        closeBtn.className = 'close-modal';
        closeBtn.innerHTML = '&times;';
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        // Build modal
        modalContent.appendChild(closeBtn);
        modalContent.appendChild(video);
        modal.appendChild(modalContent);
        
        // Add to DOM
        document.body.appendChild(modal);
        
        // Close when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }
    
    // Add modal styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .video-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-content {
            position: relative;
            width: 80%;
            max-width: 800px;
        }
        .modal-content video {
            width: 100%;
            outline: none;
        }
        .close-modal {
            position: absolute;
            top: -40px;
            right: 0;
            color: white;
            font-size: 30px;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style);
});