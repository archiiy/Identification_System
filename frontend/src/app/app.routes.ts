import { Routes } from '@angular/router';

import { Landing } from './pages/landing/landing';
import { Login } from './pages/login/login';
import { Aadhaar } from './pages/aadhaar/aadhaar';
import { Selfie } from './pages/selfie/selfie';
import { Liveness } from './pages/liveness/liveness';
import { Result } from './pages/result/result';


export const routes: Routes = [
{
path:'',
redirectTo:'landing',
pathMatch:'full'
},

{
path:'landing',
component:Landing
},

{
path:'login',
component:Login
},

{
path:'aadhaar',
component:Aadhaar
},

{
path:'selfie',
component:Selfie
},

{
path:'liveness',
component:Liveness
},

{
path:'result',
component:Result
}

];