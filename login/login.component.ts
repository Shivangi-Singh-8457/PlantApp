import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  email:string=""
  password:string=""
  msg:any 

  constructor(private httpClient:HttpClientService) { }

  ngOnInit(): void {
  }
  onsubmit(userForm:NgForm)
  {
    this.httpClient.signin([this.email,this.password]).subscribe(res=>
    { 
      this.msg=res
      alert(this.msg);
    });
    userForm.reset();
  }
}
