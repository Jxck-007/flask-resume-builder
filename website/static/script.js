const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });
}

function datetime() {
  const now = new Date();
  const datatimestring = now.toLocaleString();
  const dtElem = document.getElementById('datetime');
  if (dtElem) dtElem.textContent = datatimestring;
}
datetime();

function popup(msg) {
  const box = document.createElement('div');
  box.className = 'flash-popup';
  box.innerText = msg;
  document.body.append(box);
  setTimeout(() => box.remove(), 3000);
}

function togglePassword(inputId, toggleElement) {
  const input = document.getElementById(inputId);
  if (input) {
    if (input.type === "password") {
      input.type = "text";
      toggleElement.textContent = "🙈";
      setTimeout(() => {
        input.type = "password";
        toggleElement.textContent = "👁️";
      }, 5000);
    } else {
      input.type = "password";
      toggleElement.textContent = "👁️";
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const nameOk = document.getElementById('name').value.trim().length >= 3;
      const emailOk = document.getElementById('email').value.trim().length >= 4;
      const pw1 = document.getElementById('password1').value;
      const pw2 = document.getElementById('password2').value;
      const lengthOk = pw1.length >= 7;
      const matchOk = pw1 === pw2;
      const upper = /[A-Z]/.test(pw1);
      const lower = /[a-z]/.test(pw1);
      const digit = /\d/.test(pw1);
      const special = /[!@#$%^&*(),.?":{}|<>]/.test(pw1);
      
      if (!nameOk) return popup('Name should contain minimum of 3 characters');
      if (!emailOk) return popup('Email should contain minimum of 4 characters');
      if (!lengthOk) return popup('Password should contain minimum of 7 characters');
      if (!upper) return popup('Password needs an uppercase letter');
      if (!lower) return popup('Password needs a lowercase letter');
      if (!digit) return popup('Password needs a digit');
      if (!special) return popup('Password needs a special character');
      if (!matchOk) return popup('Passwords must match');

      signupForm.submit();
    });
  }

  const profileImg = document.getElementById('profileImage');
  const fileInput = document.getElementById('profileUpload');
  const changeBtn = document.getElementById('profileChange');
  const removeBtn = document.getElementById('profileRemove');

  if (changeBtn && fileInput && profileImg) {
    changeBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
          profileImg.src = e.target.result;
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  }

  if (removeBtn && profileImg && fileInput) {
    removeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const defaultImg = profileImg.getAttribute('data-default');
      profileImg.src = defaultImg;
      fileInput.value = '';
      popup('Profile picture reset to default.');
    });
  }

  const editBtn = document.getElementById('edit-btn');
  const saveBtn = document.getElementById('save-btn');
  const profileForm = document.getElementById('profile-form');

  if (editBtn && saveBtn && profileForm) {
    editBtn.addEventListener('click', () => {
      profileForm.querySelectorAll('input, textarea').forEach(input => {
        if (input.id !== 'profileUpload') input.disabled = false;
      });
      saveBtn.disabled = false;
      editBtn.disabled = true;
    });

    saveBtn.addEventListener('click', () => {
      profileForm.querySelectorAll('input, textarea').forEach(input => {
        if (input.id !== 'profileUpload') input.disabled = true;
      });
      saveBtn.disabled = true;
      editBtn.disabled = false;
      popup('Changes have been saved.');
    });
  }

   const resumeForm = document.getElementById('profile-form');
  if (resumeForm) {
    const picInput = resumeForm.querySelector('input[name="profile_pic"]');
    if (picInput) {
      const previewImg = document.createElement('img');
      previewImg.id = 'resume-pic-preview';
      previewImg.style.maxWidth = '120px';
      previewImg.style.borderRadius = '50%';
      previewImg.style.margin = '10px 0';
      previewImg.alt = 'Preview';
      picInput.parentNode.insertBefore(previewImg, picInput.nextSibling);

      picInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
          const reader = new FileReader();
          reader.onload = function (e) {
            previewImg.src = e.target.result;
          };
          reader.readAsDataURL(this.files[0]);
        }
      });
    }
  }
});
