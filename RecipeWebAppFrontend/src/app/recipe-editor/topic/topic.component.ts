import { Component, OnInit, Input } from '@angular/core';
import { TopicService } from './topic.service';

@Component({
  selector: 'app-topic',
  templateUrl: './topic.component.html',
  providers: [TopicService],
  styleUrls: ['./topic.component.css']
})
export class TopicComponent implements OnInit {
  @Input('recipeId') recipeId;
  @Input('recipeLoad') recipeLoad;
  topics
  recipeSuggestions = []
  constructor(private topicService: TopicService) { }
 
  ngAfterViewInit(): void {
    this.update()
  }

  update() {
    var self = this
    self.recipeSuggestions = []
    var promise =  this.topicService.getRecipeTopicFromID(this.recipeId)
    //self.recipeSuggestions = []
    promise.then(
      (val) => {
        self.topics = val
        console.log(val[0])
        self.topics.forEach(element => {
          
          var promise2 = self.topicService.getRecipesFromTopic(element[0])
          promise2.then(
            (val2) => {
              self.recipeSuggestions = self.recipeSuggestions.concat(val2)
            },
            (err2) => console.log(err2)
          )
        });
      },
      (err) => console.log(err)
    )
  }

  ngOnInit(): void {  }

}
