import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  email:string=""
  phone:string=""
  password:string=""
  msg:any

  constructor(private httpClient:HttpClientService, private router:Router) { }

  ngOnInit(): void {
  }
  onsubmit(userForm:NgForm){
    this.httpClient.signup([this.email,this.phone,this.password]).subscribe(res=>{
      this.msg=res 
      alert(this.msg);
      this.goToPage('index');
    })
    userForm.reset();
  }
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
