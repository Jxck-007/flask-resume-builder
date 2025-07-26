const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

function togglePassword(inputId, toggleElement) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        toggleElement.textContent = "🙈"; 
        setTimeout(()=>input.type="password",5000);
        setTimeout(()=>toggleElement.textContent="👁️",5000);
    } else {
        input.type = "password";
        toggleElement.textContent = "👁️"; 
    }
}

function datetime(){
    const now=new Date();
    const datatimestring=now.toLocaleString();
    document.getElementById('datetime').textContent=datatimestring;
}
datetime()

function popup(msg){
    const box= document.createElement('div');
    box.className = 'flash-popup';
    box.innerText=msg;
    document.body.append(box);
    setTimeout(()=>box.remove(),3000);
}

document.addEventListener('DOMContentLoaded',()=>{
    const form = document.getElementById('signup-form');

form.addEventListener('submit',function (event){
    event.preventDefault();
    const nameOk= document.getElementById('name').value.trim().length>=3;
    const emailOk=document.getElementById('email').value.trim().length>=4;
    const pw1=document.getElementById('password1').value;
    const pw2=document.getElementById('password2').value;
    const lengthOk=pw1.length>=7;
    const matchOk= pw1==pw2;
    const upper   = /[A-Z]/.test(pw1);
    const lower   = /[a-z]/.test(pw1);
    const digit   = /\d/.test(pw1);
    const special = /[!@#$%^&*(),.?":{}|<>]/.test(pw1);
    if (!nameOk)        return popup('Name Should Contain minimum of 3 characters');
    if (!emailOk)       return popup('Email Should Contain minimum of 4 characters');
    if (!lengthOk)      return popup('Password Should Contain minimum of 7 characters');
    if (!upper)         return popup('Password Needs an uppercase letter');
    if (!matchOk)       return popup('Passwords must match');
    if (!digit)         return popup('Password Needs a digit');
    if (!lower)         return popup('Password Needs a lowercase letter');
    if (!special)       return popup('Password Needs a special char');
    form.submit();
    });
});

document.addEventListener('DOMContentLoaded', () => {
  const changeBtn = document.getElementById('profileChange');
  const fileInput = document.getElementById('profileUpload');
  const profileImg = document.getElementById('profileImage');
  const removeBtn = document.getElementById('profileRemove');
  changeBtn.addEventListener('click', () => {
    fileInput.click();
  });
  fileInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        profileImg.src = e.target.result;
      };
      reader.readAsDataURL(this.files[0]);
    }
  });
  removeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const defaultImg = profileImg.getAttribute('data-default');
    profileImg.src = defaultImg;
    fileInput.value = '';
    popup('Profile picture reset to default.');
  });

  const editBtn = document.getElementById('edit-btn');
  const saveBtn = document.getElementById('save-btn');
  const form = document.getElementById('profile-form');

  editBtn.addEventListener('click', () => {
    form.querySelectorAll('input, textarea').forEach(input => {
      if (input.id !== 'profileUpload') input.disabled = false;
    });
    saveBtn.disabled = false;
    editBtn.disabled = true;
  });

  saveBtn.addEventListener('click', () => {
    form.querySelectorAll('input, textarea').forEach(input => {
      if (input.id !== 'profileUpload') input.disabled = true;
    });
    saveBtn.disabled = true;
    editBtn.disabled = false;
    popup('Changes Have Been Saved');
  });
});
