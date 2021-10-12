import { Component, OnInit, ViewChild} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LDAModelService } from './ldamodel.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-ldamodel',
  templateUrl: './ldamodel.component.html',
  styleUrls: ['./ldamodel.component.css']
})
export class LdamodelComponent implements OnInit {
  id = "0"
  images = []
  model

  constructor(private activatedRoute: ActivatedRoute,
                      ldaModelService: LDAModelService,
                      sanitizer: DomSanitizer 
    ) {
    var self = this
    self.model = sanitizer.bypassSecurityTrustResourceUrl("lda_100i100p_Z");
    this.activatedRoute.queryParams.subscribe(params => {
      if ("id" in params) {
        this.id =  params["id"]
        var promise = ldaModelService.getLDAModels()
        
        
        promise.then(
          (val) => {
            if(self.id in <JSON>val) {
              self.model = "/lda_model/"+self.id+"/lda.html"
            }
            
            val[self.id].shift()
            self.images=val[self.id]
          },
          (err) => console.log(err)
        )
      }
      // Print the parameter to the console. 
    });
  }

  ngOnInit(): void {
  }
}
