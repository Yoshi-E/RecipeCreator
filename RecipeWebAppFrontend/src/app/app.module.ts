import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule, routingComponents} from './app-routing.module';
import { AppComponent, SafePipe} from './app.component';

import { AlertModule } from './_alert';
import { TestComponent } from './test/test.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { RecipeEditorModule} from './recipe-editor/recipe-editor.module';
import { SearchComponent } from './search/search.component';
import { RecipeSearchComponent } from './recipe-search/recipe-search.component';
import { ResultComponent } from './recipe-search/result/result.component';
import { LdamodelComponent } from './ldamodel/ldamodel.component';

@NgModule({
  declarations: [
    AppComponent,
    TestComponent,
    HeaderComponent,
    FooterComponent,
    routingComponents,
    SafePipe,
    SearchComponent,
    RecipeSearchComponent,
    ResultComponent,
    LdamodelComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
	  FormsModule,
    HttpClientModule,
    RecipeEditorModule,
    AlertModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
