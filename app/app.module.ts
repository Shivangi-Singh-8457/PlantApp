import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IndexComponent } from './index/index.component';
import { DetectComponent } from './detect/detect.component';
//import { HttpClientComponent } from './service/http-client/http-client.component';
import { HttpClientService } from './service/http-client.service';
import { HttpInterceptorService } from './service/http-interceptor.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { LearningModuleComponent } from './learning-module/learning-module.component';
import { AddleafComponent } from './addleaf/addleaf.component';
import { LearnComponent } from './learn/learn.component';
import { ReviewComponent } from './review/review.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';
import { ForgotPswdComponent } from './forgot-pswd/forgot-pswd.component';

@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    DetectComponent,
    LearningModuleComponent,
    AddleafComponent,
    LearnComponent,
    ReviewComponent,
    RegisterComponent,
    LoginComponent,
    LogoutComponent,
    ForgotPswdComponent,
    //HttpClientComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: HttpInterceptorService, multi: true },],
  bootstrap: [AppComponent]
})
export class AppModule { }
