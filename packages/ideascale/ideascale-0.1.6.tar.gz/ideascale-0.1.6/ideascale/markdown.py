import pandas as pd
from jinja2 import Template
from collections import Counter

class markdown:
    """
    This mark down class is used for generate .md file for IdeaScale Project.


    """
    def __init__(self):
        self.template=Template("Tesla Ideas - Community Highlights \n \n" 
                               
                               "## Executive Summary \n"
                            
                               '## The Challenge \n'
                                "You've shown your commitment to innovation by providing IdeaScale to your workforce, your customer community, and your collaborators. This expansive IdeaScale Community has provided you with ideas that allow for continuous innovation, but only if you are able to organize them and take action. \n \n \n"
                                
                                'Fundamental to the process of acting on ideas is being able to discover what your community has demonstrated to be popular, salient, and impactful.   Similarly, innovation is what people do, not software or databases, so understanding the Members of your community is essential for driving innovation by assembling teams of people with demonstrated interest and expertise. \n'
                               
                               '### Proposed Solution \n'
                               'IdeaScale is committed to providing the tools that will nurture the entire innovation life cycle of an idea from capture to project completion. In that spirit, we are offering this data analysis service which characterizes the key assets in your Community - your Ideas and Members. \n \n'
                               
                               "With IdeaScale, you have experienced how a platform where everyone involved in this innovation process can provide their input for future directions. The Tesla Ideas community at IdeaScale has a wide variety of participants who suggest Ideas based on their experience and desire of what future innovations should be like. \n \n"
                               
                               "We have built a Natural Language Processing (NLP) system which can categorize and highlight the best ideas and contriburors through machine learning on the content and user interactions.  \n \n"
                               
                               "Through this data management we will be able to provide you highlights of some of the innovative Ideas, which might add value to the company and the society as a whole. These Ideas are direct from both the minds of your employees and people all over the globe who strive for change.\n \n"
                               
                               "In addition to characterizing the Ideas and Members of your community, we also highlight Terms and Topic that are discussed repeatedly, offering you the ability to discover what future project areas are brewing in the minds of all contributors. \n \n"
                               
                               "### Value \n"
                               "The overall purpose of this activity is to provide executives with information that is important to their decision making. With the best Ideas filtered through our system from the Tesla Ideas community, you will be able to get the thoughts and perspective from both the employee and customer point of view. These Ideas if nurtured along with the company vision will help create more value and prestige to your innovative brand. \n"

                               "### Final thoughts & next steps \n"
                               "Ideas can shape lives, through this activity we are reaching global participants and creating an interactive community for their input to help us innovate and provide your prestigious company with relevant information which can help the company for not only improving the current products/processes but also create opportunities to tap into the markets which have all the potential to embrace this change. Let us help you in exploring the future directions for the company through Innovative Ideas and make the future better. \n"
                                
                               "## Highlights \n"
                               
                               "### Topics and Ideas \n"
                               
                               "{{topic_tocs_total_ideas}} ideas have been classified into {{topic_tocs_total_topics}} \n \n"
                               
                               "Some notable topics: \n \n"
                            
                               
                               '{% for topic_title, ideas in topic_toc_zip %}  - {{topic_title}} ({{ideas}} ideas) \n {% endfor %}'
                                                              
                               "\n"

                               "### Commonly used terms \n\n"
                               "86 Terms are both commonly used and highly specific.  These terms are specific to existing Tesla products or concepts and are frequently discussed in the community. \n \n"
                               
                               "Some notable terms are : \n\n"
                               "TODO \n\n"
                               
                               "### Roles \n\n"
                               "{{total_roles}} Roles that are potentially important from both; company and customer perspective for improvement of products and experiences. \n \n"
                               
                               "Some notable roles are: \n \n"
                               "{% for role_value, role_count in role_zip %} - {{role_value}} ({{role_count}} ideas) \n {% endfor %}"
                               
                               "\n"
                               "### Tesla product features \n\n"
                               "Tesla product features that are both significant and commonly discussed in the community. These may be important to the executive management to analyze user experience alignment. \n \n"
                               
                               "Some notable features are: \n\n"
                               
                               '{% for product_value, product_count in product_zip %} - {{product_value}} ({{product_count}} ideas) \n {% endfor %}' 
                               
                               "\n"
                               
                               "### Top contributors \n\n"
                               
                               "These are the top contributors; based on their reputation and input in the community. These members create and add value to the overall discussions on different Tesla products and concepts. \n \n"
                               
                               "Some of the top contributors are: \n\n"
                               
                               '{% for contributer in contributers %}  - {{contributer}} \n {% endfor %}'
                               "\n"
                               
                               "###  Ranking of Ideas based on Reputation \n\n"
                               
                               "#### A.  Top ranked ideas and their Selection and Implementation status \n\n"
                               
                                "TODO \n\n"
                               
                               "#### B.  Top ranked ideas that have been marked Selected and completed \n\n"
                               
                               "TODO \n\n"
                               
                               "#### C.  Top ranked ideas that have been marked Selected but not completed \n\n"

                               "TODO \n\n"
                               
                               "### Tags in common usage \n\n"

                               "{{total_tag}} tags are in common use, some of the notable and recurring tags are: \n\n"
                               
                               '{% for tag_value,tag_count in tag_zip %}  - {{tag_value}} ({{tag_count}} ideas) \n {% endfor %}'
                               
                               "\n"
                               
                               "### The Trending Terms in your community over the past month are (TBD):\n\n"
                               "TODO \n\n"
                               
                               "### Novel Terms \n\n"
                               
                               "Based on novelty, some interesting terms are: \n\n"
                               "TODO \n\n"
                               
                               "### Locations \n\n"

                                "Significant Locations mentioned in the community are: \n\n"
                               "TODO \n\n"

                                "### People / Person \n\n"
                               
                               "Significant people mentioned in community discussion are : \n\n"
                                "TODO \n\n"
                               
                               "### Acronyms \n\n"
                               "Some significant Acronyms are: \n\n"
                               )

    def topics_toc(self,file,to_rank):
        ind_list=[i for i in range(to_rank+1)]
        df=pd.read_csv(file,index_col="topic_id")
        self.topic_tocs_total_ideas=sum(df["total_ideas"].tolist())
        self.topic_tocs_total_topics=len(df.index.tolist())
        df=df.loc[df.index[ind_list]]
        self.topic_toc_tile=df["topic_title"].tolist()
        self.topic_toc_ideas=df["total_ideas"].tolist()
        self.topic_toc_zip=zip(self.topic_toc_tile,self.topic_toc_ideas)
    def mavens(self,file,to_rank):
        ind_list=[i for i in range(to_rank+1)]
        df=pd.read_csv(file,index_col="Rank")
        df=df.loc[df.index[ind_list]]
        self.contributors=df["Member Name"]

    def tags(self,file,to_rank):
        df=pd.read_csv(file,index_col="tag")

        ## wrap distint tag
        group_df=df.groupby(["tag"]).size().sort_values(ascending=False).reset_index(name='count')
        self.total_tag=len(group_df.index.tolist())
        group_df=group_df[0:to_rank]
        tag_value=group_df["tag"]
        tag_count=group_df["count"]
        self.tag_zip=zip(tag_value,tag_count)
    def terms(self,file,to_rank):
        df=pd.read_csv(file,index_col=None)
        df=df[["system_asserted_tag","entity"]]
        role_df=df.loc[df["system_asserted_tag"]=="ROLE"]
        product_df=df.loc[df["system_asserted_tag"]=="PRODUCT"]
        role_group=role_df.groupby(["entity"]).size().sort_values(ascending=False).reset_index(name='count')
        self.total_role=len(role_group["count"].tolist())
        product_group=product_df.groupby(["entity"]).size().sort_values(ascending=False).reset_index(name='count')
        self.total_group=len(product_group["count"].tolist())
        role_group=role_group[0:to_rank]
        product_group=product_group[0:to_rank]
        self.role_value=role_group["entity"]
        self.role_count=role_group["count"]
        self.product_value=product_group["entity"]
        self.product_count=product_group["count"]
        self.role_zip=zip(self.role_value,self.role_count)
        self.product_zip=zip(self.product_value,self.product_count)
    def write(self,file_name):
        """
        This function will create a readme.md file which is generated by the self.template

        """
        with open(file_name,'w') as f:
            f.write(self.template.render(topic_tocs_total_ideas=self.topic_tocs_total_ideas,topic_tocs_total_topics=self.topic_tocs_total_topics,topic_toc_zip=self.topic_toc_zip,contributers=self.contributors,total_tag=self.total_tag,tag_zip=self.tag_zip, total_roles=self.total_role,role_zip=self.role_zip,product_zip=self.product_zip))

