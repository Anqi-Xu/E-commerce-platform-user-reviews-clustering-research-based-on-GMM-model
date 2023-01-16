# E-commerce-platform-user-reviews-clustering-research-based-on-GMM-model
This paper focuses on the algorithmic study of Gaussian mixture clustering model and the practical application of Gaussian mixture clustering model.

Firstly, we crawled the user reviews of laptops in Jingdong Mall through Python crawler technology. The original review data of 185289 items were obtained. After completing the related pre-processing work, we got 147,586 valid reviews, including 9033 reviews of Huawei laptops and 7321 reviews of Apple laptops.

On the basis of data cleaning, this paper adopts the Chinese word separation method based on the Hidden Markov Model of Jieba exact pattern word separation to complete the word separation processing of valid reviews. After analyzing the deactivated words, word frequency statistics, and word cloud graph features, we extracted the topics of Huawei and Apple user reviews by LDA model, and clustered the reviews of Huawei and Apple users under the topic of hardware configuration, respectively. behavior and play a role in guiding product improvement.
