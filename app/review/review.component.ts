import { Component, OnInit } from '@angular/core';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.scss']
})
export class ReviewComponent implements OnInit {

  folderlist:any=[];

  constructor(private httpClient:HttpClientService){
    this.httpClient.getfolders().subscribe(
      res=>{
        this.folderlist=res;
        console.log(this.folderlist)
      }
     )
   }

  ngOnInit(): void {
  }

}
