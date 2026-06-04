
      function showSidebar(){
        const sidebar=document.querySelector('.sidebar')
        sidebar.style.display='flex'
      }
      function hideSidebar(){
        const sidebar=document.querySelector('.sidebar')
        sidebar.style.display='none'
      }

 document.addEventListener("DOMContentLoaded", () => {

  const faqQuestions =
  document.querySelectorAll(".faq-question");

  faqQuestions.forEach(question => {

    question.addEventListener("click", () => {

      const answer =
      question.nextElementSibling;

      const icon =
      question.querySelector("span");

      if(answer.style.maxHeight){

        answer.style.maxHeight = null;
        icon.innerHTML = "+";
      }

      else{

        answer.style.maxHeight =
        answer.scrollHeight + "px";

        icon.innerHTML = "−";
      }

    });

  });

});


const bestDealBtns =
document.querySelectorAll(".best-deal");

bestDealBtns.forEach((button) => {

  button.addEventListener("click", () => {

    const popup =
    button.parentElement.querySelector(".popup");

    popup.style.display = "flex";

  });

});


// CLOSE POPUP
function closePopup(){

  document.querySelectorAll(".popup").forEach((popup) => {

    popup.style.display = "none";

  });

}

// FORM SUBMIT
document.querySelectorAll(".popup form").forEach((form) => {

  form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const formData = new FormData(form);

    const data = {
      name: formData.get("name"),
      phone: formData.get("phone"),
      city: formData.get("city"),
      requirement: formData.get("requirement")
    };

    console.log(data);

    alert("Thank you for trusting us! We will contact you soon.");

    form.reset();

    closePopup();

  });

});