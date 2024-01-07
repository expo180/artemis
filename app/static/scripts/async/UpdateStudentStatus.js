document.addEventListener('DOMContentLoaded', function () {
    const changeStatusBtn = document.getElementById('changeStatusBtn');
    if (changeStatusBtn) {
      changeStatusBtn.addEventListener('click', function () {
        const studentId = this.getAttribute('data-student-id');
  
        if (studentId) {
          this.disabled = true;
          this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Changing...';
  
          // Make an AJAX request
          fetch(`https://bit-t2kb.onrender.com/api/change_status/${studentId}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                this.innerHTML = 'Done <i class="bi bi-check"></i>';
                this.classList.remove('btn-outline-primary');
              } else {
                console.error('Failed to change status');
                this.disabled = false;
                this.innerHTML = 'Change status';
              }
            })
            .catch(error => {
              console.error('Error:', error)
              this.disabled = false;
              this.innerHTML = '<span>×</span> Retry';
            });
        } else {
          console.error('Invalid studentId');
        }
      });
    }
});