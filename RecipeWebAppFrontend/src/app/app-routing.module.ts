import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { TestComponent } from './test/test.component';
import { RecipeEditorComponent } from './recipe-editor/recipe-editor.component';
import { SearchComponent } from './search/search.component';
import { RecipeSearchComponent } from './recipe-search/recipe-search.component';
import { LdamodelComponent } from './ldamodel/ldamodel.component';

const routes: Routes = [
  { path: '', component: TestComponent},
  { path: 'test', component: RecipeEditorComponent},
  { path: 'ingredient', component: SearchComponent},
  { path: 'search', component: RecipeSearchComponent},
  { path: 'lda', component: LdamodelComponent},
  { path: '**', component: PageNotFoundComponent},  // Wildcard route for a 404 page
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [RecipeEditorComponent, TestComponent, PageNotFoundComponent]