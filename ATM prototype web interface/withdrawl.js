class PinLogin {
    constructor ({el, loginEndpoint, redirectTo, maxNumbers = 10}) {
        this.el = { // it means this el is going to contain all of the element we are going to need like numpad nad textbox  
            main: el,
            numPad: el.querySelector(".pin-login__numpad"),
            textDisplay: el.querySelector(".pin-login__text")
        };

        this.loginEndpoint = loginEndpoint;
        this.redirectTo = redirectTo;
        this.maxNumbers = maxNumbers;
        this.value = ""; // this value is the value that is going to be sent in login.php and this will change when user inputs the number

        this._generatePad(); // tell js to generate pad function hai
    }

    _generatePad() {
        const padLayout = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "backspace", "0", "done"
        ];
        // since we have generated the key we can now loop each of the key
        padLayout.forEach(key => {
            const insertBreak = key.search(/[369]/) !== -1; // if key search will not able to find 3 6 9 then it will return -1 and if gets 3 6 9 then line will bareak
            const keyEl = document.createElement("div");

            keyEl.classList.add("pin-login__key"); // for css we have added class pin-login__key
            
            keyEl.classList.toggle("material-icons", isNaN(key)); // if a key is not a number then we are adding class material_icon
            
            keyEl.textContent = key; 
           
            keyEl.addEventListener("click", () => { this._handleKeyPress(key) });// we are defining a function handleKeyPress here. so it is going to handle all the inputs user inputs 
            this.el.numPad.appendChild(keyEl);

            if (insertBreak) {
                this.el.numPad.appendChild(document.createElement("br")); //3 6 9 ke baad Br hoga
            }
        });
    }

    _handleKeyPress(key) {
        switch (key) {
            case "backspace":
                this.value = this.value.substring(0, this.value.length - 1); // to do backspace
                break;
            case "done":
                this._attemptLogin(); // when done attempt to Login
                break;
            default:
                if (this.value.length < this.maxNumbers && !isNaN(key)) { //!isNaN(key) is written so that no alphabet can be written in numpad 
                    this.value += key; // defining the key 
                }
                break;
        }

        this._updateValueText();  // what ever we click it will show in textbox
    }

    _updateValueText() {
        this.el.textDisplay.value = this.value; // dispay on textbox and not on the textbox. if we want to see what's on the textbox: document.querySelector(".pin-login__text"). it will show 1234  ---- in console
        this.el.textDisplay.classList.remove("pin-login__text--error");
    }

    _attemptLogin() {
        if (this.value.length > 0) {
            fetch(this.loginEndpoint, { //fetch the login request
                method: "post",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `pincode=${this.value}`
            }).then(response => {
                
                    window.location.href = this.redirectTo;
                 
                
            })
        }
    }
}

new PinLogin({
    el: document.getElementById("mainPinLogin"),
    loginEndpoint: "", // dashboard.html
    redirectTo: "thankyou.html",
    maxNumbers: 4
});