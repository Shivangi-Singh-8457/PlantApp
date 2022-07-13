import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  
  login_flag:any;

  constructor(private httpClient:HttpClientService, private router: Router){
    
  }

  ngOnInit(): void {
    this.httpClient.checksignin().subscribe(
      res=>{
        this.login_flag=res
        console.log(this.login_flag);
        console.log(typeof this.login_flag); 
    });
  }
    
  goToPage(this:any, pageName:string){
    this.router.navigate([`${pageName}`]);
  }
}
 



