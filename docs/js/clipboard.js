document.addEventListener('DOMContentLoaded', function() {
  const copyButtons = document.querySelectorAll('.copy-btn');
  
  copyButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const textToCopy = this.dataset.copy;
      const label = this.querySelector('.copy-label');
      
      navigator.clipboard.writeText(textToCopy).then(function() {
        // Feedback
        const originalText = label.textContent;
        label.textContent = 'Kopiert!';
        btn.classList.add('copied');
        
        setTimeout(function() {
          label.textContent = originalText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        // Fallback: Auswählen
        const iban = document.getElementById('iban');
        const range = document.createRange();
        range.selectNode(iban);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
      });
    });
  });
});