import { Component } from '@angular/core';

import {

Router

} from '@angular/router';

import {

FormsModule

} from '@angular/forms';


@Component({

selector:'app-login',

imports:[

FormsModule

],

templateUrl:'./login.html',

styleUrl:'./login.css'

})

export class Login{

email='';

constructor(

private router:Router

){}


continue(){

if(

!this.email.includes('@')

){

alert(

'Enter valid email'

);

return;

}


localStorage.setItem(

'email',

this.email

);


this.router.navigate(

['/aadhaar']

);

}

}