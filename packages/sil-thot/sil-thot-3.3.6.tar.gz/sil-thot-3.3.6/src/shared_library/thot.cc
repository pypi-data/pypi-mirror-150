// thot.cpp : Defines the exported functions for the DLL application.
//

#include "thot.h"

#include "incr_models/IncrJelMerNgramLM.h"
#include "incr_models/WordPenaltyModel.h"
#include "phrase_models/WbaIncrPhraseModel.h"
#include "stack_dec/BasePbTransModel.h"
#include "stack_dec/KbMiraLlWu.h"
#include "stack_dec/LangModelInfo.h"
#include "stack_dec/MiraBleu.h"
#include "stack_dec/PhrLocalSwLiTm.h"
#include "stack_dec/PhraseModelInfo.h"
#include "stack_dec/SwModelInfo.h"
#include "stack_dec/TranslationMetadata.h"
#include "stack_dec/_phrSwTransModel.h"
#include "stack_dec/_phraseBasedTransModel.h"
#include "stack_dec/multi_stack_decoder_rec.h"
#include "sw_models/FastAlignModel.h"
#include "sw_models/HmmAlignmentModel.h"
#include "sw_models/Ibm1AlignmentModel.h"
#include "sw_models/Ibm2AlignmentModel.h"
#include "sw_models/Ibm3AlignmentModel.h"
#include "sw_models/Ibm4AlignmentModel.h"
#include "sw_models/IncrAlignmentModel.h"
#include "sw_models/IncrHmmAlignmentModel.h"
#include "sw_models/IncrIbm1AlignmentModel.h"
#include "sw_models/IncrIbm2AlignmentModel.h"

#include <sstream>

struct SmtModelInfo
{
  SwModelInfo* swModelInfoPtr;
  PhraseModelInfo* phrModelInfoPtr;
  LangModelInfo* langModelInfoPtr;
  PhrLocalSwLiTm* smtModelPtr;
  BaseTranslationMetadata<PhrLocalSwLiTm::HypScoreInfo>* trMetadataPtr;
  BaseScorer* scorerPtr;
  BaseLogLinWeightUpdater* llWeightUpdaterPtr;
  std::string lmFileName;
  std::string tmFileNamePrefix;
};

struct DecoderInfo
{
  SmtModelInfo* smtModelInfoPtr;
  PhrLocalSwLiTm* smtModelPtr;
  _stackDecoderRec<PhrLocalSwLiTm>* stackDecoderPtr;
  BaseTranslationMetadata<PhrLocalSwLiTm::HypScoreInfo>* trMetadataPtr;
};

struct LlWeightUpdaterInfo
{
  BaseScorer* baseScorerPtr;
  BaseLogLinWeightUpdater* llWeightUpdaterPtr;
};

struct WordGraphInfo
{
  std::string wordGraphStr;
  Score initialStateScore;
};

unsigned int copyString(const std::string& result, char* cstring, unsigned int capacity)
{
  if (cstring != NULL)
  {
    size_t len = result.copy(cstring, (size_t)capacity);
    if (len < capacity)
      cstring[len] = '\0';
  }
  return (unsigned int)result.length();
}

std::vector<WordIndex> getWordIndices(AlignmentModel* alignmentModel, const char* sentence, bool source)
{
  std::vector<WordIndex> wordIndices;
  size_t i = 0;
  std::string s;
  while (sentence[i] != 0)
  {
    s = "";
    while (sentence[i] == ' ' && sentence[i] != 0)
    {
      ++i;
    }
    while (sentence[i] != ' ' && sentence[i] != 0)
    {
      s = s + sentence[i];
      ++i;
    }
    if (s != "")
    {
      WordIndex wordIndex = source ? alignmentModel->stringToSrcWordIndex(s) : alignmentModel->stringToTrgWordIndex(s);
      wordIndices.push_back(wordIndex);
    }
  }
  return wordIndices;
}

AlignmentModel* createAlignmentModel(enum AlignmentModelType type, AlignmentModel* model = nullptr)
{
  switch (type)
  {
  case AlignmentModelType::Ibm1:
    return new Ibm1AlignmentModel();
  case AlignmentModelType::Ibm2:
    if (model != nullptr)
    {
      auto ibm1Model = dynamic_cast<Ibm1AlignmentModel*>(model);
      if (ibm1Model != nullptr)
        return new Ibm2AlignmentModel(*ibm1Model);
    }
    return new Ibm2AlignmentModel();
  case AlignmentModelType::Hmm:
    if (model != nullptr)
    {
      auto ibm1Model = dynamic_cast<Ibm1AlignmentModel*>(model);
      if (ibm1Model != nullptr)
        return new HmmAlignmentModel(*ibm1Model);
    }
    return new HmmAlignmentModel();
  case AlignmentModelType::Ibm3:
    if (model != nullptr)
    {
      auto hmmModel = dynamic_cast<HmmAlignmentModel*>(model);
      if (hmmModel != nullptr)
        return new Ibm3AlignmentModel(*hmmModel);
      auto ibm2Model = dynamic_cast<Ibm2AlignmentModel*>(model);
      if (ibm2Model != nullptr)
        return new Ibm3AlignmentModel(*ibm2Model);
    }
    return new Ibm3AlignmentModel();
  case AlignmentModelType::Ibm4:
    if (model != nullptr)
    {
      auto ibm3Model = dynamic_cast<Ibm3AlignmentModel*>(model);
      if (ibm3Model != nullptr)
        return new Ibm4AlignmentModel(*ibm3Model);
    }
    return new Ibm4AlignmentModel();
  case AlignmentModelType::IncrIbm1:
    return new IncrIbm1AlignmentModel();
  case AlignmentModelType::IncrIbm2:
    return new IncrIbm2AlignmentModel();
  case AlignmentModelType::IncrHmm:
    return new IncrHmmAlignmentModel();
  case AlignmentModelType::FastAlign:
    return new FastAlignModel();
  }
  return nullptr;
}

extern "C"
{
  void* smtModel_create(enum AlignmentModelType alignmentModelType)
  {
    auto smtModelInfo = new SmtModelInfo;

    smtModelInfo->langModelInfoPtr = new LangModelInfo;
    smtModelInfo->phrModelInfoPtr = new PhraseModelInfo;
    smtModelInfo->swModelInfoPtr = new SwModelInfo;

    smtModelInfo->langModelInfoPtr->wpModelPtr = new WordPenaltyModel;
    smtModelInfo->langModelInfoPtr->lModelPtr = new IncrJelMerNgramLM;
    smtModelInfo->phrModelInfoPtr->invPbModelPtr = new WbaIncrPhraseModel;
    smtModelInfo->swModelInfoPtr->swAligModelPtrVec.push_back(createAlignmentModel(alignmentModelType));
    smtModelInfo->swModelInfoPtr->invSwAligModelPtrVec.push_back(createAlignmentModel(alignmentModelType));
    smtModelInfo->scorerPtr = new MiraBleu;
    smtModelInfo->llWeightUpdaterPtr = new KbMiraLlWu;
    smtModelInfo->trMetadataPtr = new TranslationMetadata<PhrScoreInfo>;

    // Link scorer to weight updater
    if (!smtModelInfo->llWeightUpdaterPtr->link_scorer(smtModelInfo->scorerPtr))
    {
      std::cerr << "Error: Scorer class could not be linked to log-linear weight "
                   "updater"
                << std::endl;
      return NULL;
    }

    // Instantiate smt model
    smtModelInfo->smtModelPtr = new PhrLocalSwLiTm;

    // Link pointers
    smtModelInfo->smtModelPtr->link_lm_info(smtModelInfo->langModelInfoPtr);
    smtModelInfo->smtModelPtr->link_pm_info(smtModelInfo->phrModelInfoPtr);
    smtModelInfo->smtModelPtr->link_swm_info(smtModelInfo->swModelInfoPtr);
    smtModelInfo->smtModelPtr->link_trans_metadata(smtModelInfo->trMetadataPtr);

    return smtModelInfo;
  }

  bool smtModel_loadTranslationModel(void* smtModelHandle, const char* tmFileNamePrefix)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    if (strcmp(smtModelInfo->tmFileNamePrefix.c_str(), tmFileNamePrefix) == 0)
      return true;

    smtModelInfo->tmFileNamePrefix = tmFileNamePrefix;
    return smtModelInfo->smtModelPtr->loadAligModel(tmFileNamePrefix);
  }

  bool smtModel_loadLanguageModel(void* smtModelHandle, const char* lmFileName)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    if (strcmp(smtModelInfo->lmFileName.c_str(), lmFileName) == 0)
      return true;

    smtModelInfo->lmFileName = lmFileName;
    return smtModelInfo->smtModelPtr->loadLangModel(lmFileName);
  }

  void smtModel_setNonMonotonicity(void* smtModelHandle, unsigned int nomon)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    smtModelInfo->smtModelPtr->set_U_par(nomon);
  }

  void smtModel_setW(void* smtModelHandle, float w)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    smtModelInfo->smtModelPtr->set_W_par(w);
  }

  void smtModel_setA(void* smtModelHandle, unsigned int a)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    smtModelInfo->smtModelPtr->set_A_par(a);
  }

  void smtModel_setE(void* smtModelHandle, unsigned int e)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    smtModelInfo->smtModelPtr->set_E_par(e);
  }

  void smtModel_setHeuristic(void* smtModelHandle, unsigned int heuristic)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    smtModelInfo->smtModelPtr->setHeuristic(heuristic);
  }

  void smtModel_setOnlineTrainingParameters(void* smtModelHandle, unsigned int algorithm,
                                            unsigned int learningRatePolicy, float learnStepSize, unsigned int emIters,
                                            unsigned int e, unsigned int r)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    OnlineTrainingPars otPars;
    otPars.onlineLearningAlgorithm = algorithm;
    otPars.learningRatePolicy = learningRatePolicy;
    otPars.learnStepSize = learnStepSize;
    otPars.emIters = emIters;
    otPars.E_par = e;
    otPars.R_par = r;
    smtModelInfo->smtModelPtr->setOnlineTrainingPars(otPars, 0);
  }

  void smtModel_setWeights(void* smtModelHandle, const float* weights, unsigned int capacity)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    std::vector<float> weightsVec;
    for (unsigned int i = 0; i < capacity; ++i)
      weightsVec.push_back(weights[i]);
    smtModelInfo->smtModelPtr->setWeights(weightsVec);
  }

  void* smtModel_getSingleWordAlignmentModel(void* smtModelHandle)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    return smtModelInfo->swModelInfoPtr->swAligModelPtrVec[0];
  }

  void* smtModel_getInverseSingleWordAlignmentModel(void* smtModelHandle)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    return smtModelInfo->swModelInfoPtr->invSwAligModelPtrVec[0];
  }

  bool smtModel_saveModels(void* smtModelHandle)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);
    if (!smtModelInfo->smtModelPtr->printAligModel(smtModelInfo->tmFileNamePrefix))
      return false;

    return smtModelInfo->smtModelPtr->printLangModel(smtModelInfo->lmFileName);
  }

  void smtModel_close(void* smtModelHandle)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);

    smtModelInfo->smtModelPtr->clear();

    // Delete pointers
    delete smtModelInfo->langModelInfoPtr->lModelPtr;
    delete smtModelInfo->langModelInfoPtr->wpModelPtr;
    delete smtModelInfo->langModelInfoPtr;
    delete smtModelInfo->phrModelInfoPtr->invPbModelPtr;
    delete smtModelInfo->phrModelInfoPtr;
    delete smtModelInfo->swModelInfoPtr->swAligModelPtrVec[0];
    delete smtModelInfo->swModelInfoPtr->invSwAligModelPtrVec[0];
    delete smtModelInfo->swModelInfoPtr;
    delete smtModelInfo->smtModelPtr;
    delete smtModelInfo->llWeightUpdaterPtr;
    delete smtModelInfo->scorerPtr;
    delete smtModelInfo->trMetadataPtr;

    delete smtModelInfo;
  }

  void* decoder_create(void* smtModelHandle)
  {
    auto smtModelInfo = static_cast<SmtModelInfo*>(smtModelHandle);

    auto decoderInfo = new DecoderInfo;

    decoderInfo->smtModelInfoPtr = smtModelInfo;

    decoderInfo->stackDecoderPtr = new multi_stack_decoder_rec<PhrLocalSwLiTm>;

    // Create statistical machine translation model instance (it is
    // cloned from the main one)
    BaseSmtModel<PhrLocalSwLiTm::Hypothesis>* baseSmtModelPtr = smtModelInfo->smtModelPtr->clone();
    decoderInfo->smtModelPtr = dynamic_cast<PhrLocalSwLiTm*>(baseSmtModelPtr);

    decoderInfo->trMetadataPtr = new TranslationMetadata<PhrScoreInfo>;
    decoderInfo->smtModelPtr->link_trans_metadata(decoderInfo->trMetadataPtr);

    decoderInfo->stackDecoderPtr->link_smt_model(decoderInfo->smtModelPtr);

    decoderInfo->stackDecoderPtr->useBestScorePruning(true);

    return decoderInfo;
  }

  void decoder_setS(void* decoderHandle, unsigned int s)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);
    decoderInfo->stackDecoderPtr->set_S_par(s);
  }

  void decoder_setBreadthFirst(void* decoderHandle, bool breadthFirst)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);
    decoderInfo->stackDecoderPtr->set_breadthFirst(breadthFirst);
  }

  void decoder_setG(void* decoderHandle, unsigned int g)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);
    decoderInfo->stackDecoderPtr->set_G_par(g);
  }

  void decoder_close(void* decoderHandle)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    delete decoderInfo->smtModelPtr;
    delete decoderInfo->stackDecoderPtr;
    delete decoderInfo->trMetadataPtr;

    delete decoderInfo;
  }

  void* decoder_translate(void* decoderHandle, const char* sentence)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    auto result = new TranslationData;

    // Use translator
    PhrLocalSwLiTm::Hypothesis hyp = decoderInfo->stackDecoderPtr->translate(sentence);

    std::vector<std::pair<PositionIndex, PositionIndex>> amatrix;
    // Obtain phrase alignment
    decoderInfo->smtModelPtr->aligMatrix(hyp, amatrix);
    decoderInfo->smtModelPtr->getPhraseAlignment(amatrix, result->sourceSegmentation, result->targetSegmentCuts);
    result->target = decoderInfo->smtModelPtr->getTransInPlainTextVec(hyp, result->targetUnknownWords);
    result->score = decoderInfo->smtModelPtr->getScoreForHyp(hyp);
    result->scoreComponents = decoderInfo->smtModelPtr->scoreCompsForHyp(hyp);

    return result;
  }

  unsigned int decoder_translateNBest(void* decoderHandle, unsigned int n, const char* sentence, void** results)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    // Enable word graph generation
    decoderInfo->stackDecoderPtr->enableWordGraph();

    // Use translator
    decoderInfo->stackDecoderPtr->translate(sentence);
    WordGraph* wg = decoderInfo->stackDecoderPtr->getWordGraphPtr();

    decoderInfo->stackDecoderPtr->disableWordGraph();

    std::vector<TranslationData> translations;
    wg->obtainNbestList(n, translations);

    for (unsigned int i = 0; i < n && i < translations.size(); ++i)
      results[i] = new TranslationData(translations[i]);

    return (unsigned int)translations.size();
  }

  void* decoder_getWordGraph(void* decoderHandle, const char* sentence)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    auto result = new WordGraphInfo;

    decoderInfo->stackDecoderPtr->useBestScorePruning(false);

    // Enable word graph generation
    decoderInfo->stackDecoderPtr->enableWordGraph();

    // Use translator
    PhrLocalSwLiTm::Hypothesis hyp = decoderInfo->stackDecoderPtr->translate(sentence);
    WordGraph* wg = decoderInfo->stackDecoderPtr->getWordGraphPtr();

    decoderInfo->stackDecoderPtr->disableWordGraph();

    decoderInfo->stackDecoderPtr->useBestScorePruning(true);

    if (decoderInfo->smtModelPtr->isComplete(hyp))
    {
      // Remove non-useful states from word-graph
      wg->obtainWgComposedOfUsefulStates();
      wg->orderArcsTopol();

      std::ostringstream outS;
      wg->print(outS, false);
      result->wordGraphStr = outS.str();
      result->initialStateScore = wg->getInitialStateScore();
    }
    else
    {
      result->wordGraphStr = "";
      result->initialStateScore = 0;
    }

    return result;
  }

  void* decoder_getBestPhraseAlignment(void* decoderHandle, const char* sentence, const char* translation)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    auto result = new TranslationData();
    PhrLocalSwLiTm::Hypothesis hyp = decoderInfo->stackDecoderPtr->translateWithRef(sentence, translation);

    std::vector<std::pair<PositionIndex, PositionIndex>> amatrix;
    // Obtain phrase alignment
    decoderInfo->smtModelPtr->aligMatrix(hyp, amatrix);
    decoderInfo->smtModelPtr->getPhraseAlignment(amatrix, result->sourceSegmentation, result->targetSegmentCuts);
    result->target = decoderInfo->smtModelPtr->getTransInPlainTextVec(hyp, result->targetUnknownWords);
    result->score = decoderInfo->smtModelPtr->getScoreForHyp(hyp);
    result->scoreComponents = decoderInfo->smtModelPtr->scoreCompsForHyp(hyp);

    return result;
  }

  bool decoder_trainSentencePair(void* decoderHandle, const char* sourceSentence, const char* targetSentence)
  {
    auto decoderInfo = static_cast<DecoderInfo*>(decoderHandle);

    // Obtain system translation
#ifdef THOT_ENABLE_UPDATE_LLWEIGHTS
    decoderInfo->stackDecoderPtr->enableWordGraph();
#endif

    PhrLocalSwLiTm::Hypothesis hyp = decoderInfo->stackDecoderPtr->translate(sourceSentence);
    std::string sysSent = decoderInfo->smtModelPtr->getTransInPlainText(hyp);

    // Add sentence to word-predictor
    decoderInfo->smtModelInfoPtr->smtModelPtr->addSentenceToWordPred(
        StrProcUtils::stringToStringVector(targetSentence));

#ifdef THOT_ENABLE_UPDATE_LLWEIGHTS
    // Train log-linear weights

    // Retrieve pointer to wordgraph
    WordGraph* wgPtr = decoderInfo->stackDecoderPtr->getWordGraphPtr();
    decoderInfo->smtModelInfoPtr->smtModelPtr->updateLogLinearWeights(targetSentence, wgPtr);

    decoderInfo->stackDecoderPtr->disableWordGraph();
#endif

    // Train generative models
    return decoderInfo->smtModelInfoPtr->smtModelPtr->onlineTrainFeatsSentPair(sourceSentence, targetSentence,
                                                                               sysSent.c_str());
  }

  unsigned int tdata_getTarget(void* dataHandle, char* target, unsigned int capacity)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    return copyString(StrProcUtils::stringVectorToString(data->target), target, capacity);
  }

  unsigned int tdata_getPhraseCount(void* dataHandle)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    return (unsigned int)data->sourceSegmentation.size();
  }

  unsigned int tdata_getSourceSegmentation(void* dataHandle, unsigned int** sourceSegmentation, unsigned int capacity)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    if (sourceSegmentation != NULL)
    {
      for (unsigned int i = 0; i < capacity && i < data->sourceSegmentation.size(); i++)
      {
        sourceSegmentation[i][0] = data->sourceSegmentation[i].first;
        sourceSegmentation[i][1] = data->sourceSegmentation[i].second;
      }
    }
    return (unsigned int)data->sourceSegmentation.size();
  }

  unsigned int tdata_getTargetSegmentCuts(void* dataHandle, unsigned int* targetSegmentCuts, unsigned int capacity)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    if (targetSegmentCuts != NULL)
    {
      for (unsigned int i = 0; i < capacity && i < data->targetSegmentCuts.size(); i++)
        targetSegmentCuts[i] = data->targetSegmentCuts[i];
    }
    return (unsigned int)data->targetSegmentCuts.size();
  }

  unsigned int tdata_getTargetUnknownWords(void* dataHandle, unsigned int* targetUnknownWords, unsigned int capacity)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    if (targetUnknownWords != NULL)
    {
      unsigned int i = 0;
      for (std::set<PositionIndex>::const_iterator it = data->targetUnknownWords.begin();
           it != data->targetUnknownWords.end() && i < capacity; ++it)
      {
        targetUnknownWords[i] = *it;
        i++;
      }
    }
    return (unsigned int)data->targetUnknownWords.size();
  }

  double tdata_getScore(void* dataHandle)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    return data->score;
  }

  unsigned int tdata_getScoreComponents(void* dataHandle, double* scoreComps, unsigned int capacity)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    for (unsigned int i = 0; i < capacity && i < data->scoreComponents.size(); i++)
      scoreComps[i] = data->scoreComponents[i];
    return (unsigned int)data->scoreComponents.size();
  }

  void tdata_destroy(void* dataHandle)
  {
    auto data = static_cast<TranslationData*>(dataHandle);
    delete data;
  }

  unsigned int wg_getString(void* wgHandle, char* wordGraphStr, unsigned int capacity)
  {
    auto wordGraph = static_cast<WordGraphInfo*>(wgHandle);
    return copyString(wordGraph->wordGraphStr, wordGraphStr, capacity);
  }

  double wg_getInitialStateScore(void* wgHandle)
  {
    auto wg = static_cast<WordGraphInfo*>(wgHandle);
    return wg->initialStateScore;
  }

  void wg_destroy(void* wgHandle)
  {
    WordGraphInfo* wordGraph = static_cast<WordGraphInfo*>(wgHandle);
    delete wordGraph;
  }

  void* swAlignModel_create(enum AlignmentModelType type, void* swAlignModelHandle)
  {
    return createAlignmentModel(type, static_cast<AlignmentModel*>(swAlignModelHandle));
  }

  void* swAlignModel_open(enum AlignmentModelType type, const char* prefFileName)
  {
    AlignmentModel* alignmentModel = createAlignmentModel(type);
    if (alignmentModel->load(prefFileName) == THOT_ERROR)
    {
      delete alignmentModel;
      return NULL;
    }
    return alignmentModel;
  }

  unsigned int swAlignModel_getMaxSentenceLength(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->getMaxSentenceLength();
  }

  void swAlignModel_setVariationalBayes(void* swAlignModelHandle, bool variationalBayes)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    alignmentModel->setVariationalBayes(variationalBayes);
  }

  bool swAlignModel_getVariationalBayes(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->getVariationalBayes();
  }

  void swAlignModel_setFastAlignP0(void* swAlignModelHandle, double p0)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto fastAlignModel = dynamic_cast<FastAlignModel*>(alignmentModel);
    if (fastAlignModel != nullptr)
      fastAlignModel->setFastAlignP0(p0);
  }

  double swAlignModel_getFastAlignP0(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto fastAlignModel = dynamic_cast<FastAlignModel*>(alignmentModel);
    if (fastAlignModel != nullptr)
      return fastAlignModel->getFastAlignP0();
    return 0;
  }

  void swAlignModel_setHmmP0(void* swAlignModelHandle, double p0)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      hmmAlignmentModel->setHmmP0(p0);
  }

  double swAlignModel_getHmmP0(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      return hmmAlignmentModel->getHmmP0();
    return 0;
  }

  void swAlignModel_setHmmLexicalSmoothingFactor(void* swAlignModelHandle, double lexicalSmoothingFactor)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      hmmAlignmentModel->setLexicalSmoothFactor(lexicalSmoothingFactor);
  }

  double swAlignModel_getHmmLexicalSmoothingFactor(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      return hmmAlignmentModel->getLexicalSmoothFactor();
    return 0;
  }

  void swAlignModel_setHmmAlignmentSmoothingFactor(void* swAlignModelHandle, double alignmentSmoothingFactor)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      hmmAlignmentModel->setHmmAlignmentSmoothFactor(alignmentSmoothingFactor);
  }

  double swAlignModel_getHmmAlignmentSmoothingFactor(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      return hmmAlignmentModel->getHmmAlignmentSmoothFactor();
    return 0;
  }

  void swAlignModel_setIbm2CompactAlignmentTable(void* swAlignModelHandle, bool compactAlignmentTable)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm2AlignmentModel = dynamic_cast<Ibm2AlignmentModel*>(alignmentModel);
    if (ibm2AlignmentModel != nullptr)
      ibm2AlignmentModel->setCompactAlignmentTable(compactAlignmentTable);
  }

  bool swAlignModel_getIbm2CompactAlignmentTable(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm2AlignmentModel = dynamic_cast<Ibm2AlignmentModel*>(alignmentModel);
    if (ibm2AlignmentModel != nullptr)
      return ibm2AlignmentModel->getCompactAlignmentTable();
    return false;
  }

  void swAlignModel_setIbm3FertilitySmoothingFactor(void* swAlignModelHandle, double fertilitySmoothingFactor)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm3AlignmentModel = dynamic_cast<Ibm3AlignmentModel*>(alignmentModel);
    if (ibm3AlignmentModel != nullptr)
      ibm3AlignmentModel->setFertilitySmoothFactor(fertilitySmoothingFactor);
  }

  double swAlignModel_getIbm3FertilitySmoothingFactor(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm3AlignmentModel = dynamic_cast<Ibm3AlignmentModel*>(alignmentModel);
    if (ibm3AlignmentModel != nullptr)
      return ibm3AlignmentModel->getFertilitySmoothFactor();
    return 0;
  }

  void swAlignModel_setIbm3CountThreshold(void* swAlignModelHandle, double countThreshold)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm3AlignmentModel = dynamic_cast<Ibm3AlignmentModel*>(alignmentModel);
    if (ibm3AlignmentModel != nullptr)
      ibm3AlignmentModel->setCountThreshold(countThreshold);
  }

  double swAlignModel_getIbm3CountThreshold(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm3AlignmentModel = dynamic_cast<Ibm3AlignmentModel*>(alignmentModel);
    if (ibm3AlignmentModel != nullptr)
      return ibm3AlignmentModel->getCountThreshold();
    return 0;
  }

  void swAlignModel_setIbm4DistortionSmoothingFactor(void* swAlignModelHandle, double distortionSmoothingFactor)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm4AlignmentModel = dynamic_cast<Ibm4AlignmentModel*>(alignmentModel);
    if (ibm4AlignmentModel != nullptr)
      ibm4AlignmentModel->setDistortionSmoothFactor(distortionSmoothingFactor);
  }

  double swAlignModel_getIbm4DistortionSmoothingFactor(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm4AlignmentModel = dynamic_cast<Ibm4AlignmentModel*>(alignmentModel);
    if (ibm4AlignmentModel != nullptr)
      return ibm4AlignmentModel->getDistortionSmoothFactor();
    return 0;
  }

  unsigned int swAlignModel_getSourceWordCount(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return (unsigned int)alignmentModel->getSrcVocabSize();
  }

  unsigned int swAlignModel_getSourceWord(void* swAlignModelHandle, unsigned int index, char* wordStr,
                                          unsigned int capacity)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return copyString(alignmentModel->wordIndexToSrcString(index), wordStr, capacity);
  }

  unsigned int swAlignModel_getSourceWordIndex(void* swAlignModelHandle, const char* word)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->stringToSrcWordIndex(word);
  }

  unsigned int swAlignModel_getTargetWordCount(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return (unsigned int)alignmentModel->getTrgVocabSize();
  }

  unsigned int swAlignModel_getTargetWord(void* swAlignModelHandle, unsigned int index, char* wordStr,
                                          unsigned int capacity)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return copyString(alignmentModel->wordIndexToTrgString(index), wordStr, capacity);
  }

  unsigned int swAlignModel_getTargetWordIndex(void* swAlignModelHandle, const char* word)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->stringToTrgWordIndex(word);
  }

  void swAlignModel_addSentencePair(void* swAlignModelHandle, const char* sourceSentence, const char* targetSentence)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);

    std::vector<std::string> source = StrProcUtils::stringToStringVector(sourceSentence);
    std::vector<std::string> target = StrProcUtils::stringToStringVector(targetSentence);

    alignmentModel->addSentencePair(source, target, 1);
    for (unsigned int j = 0; j < source.size(); j++)
      alignmentModel->addSrcSymbol(source[j]);
    for (unsigned int j = 0; j < target.size(); j++)
      alignmentModel->addTrgSymbol(target[j]);
  }

  void swAlignModel_readSentencePairs(void* swAlignModelHandle, const char* sourceFilename, const char* targetFilename,
                                      const char* countsFilename)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    std::pair<unsigned int, unsigned int> sentRange;
    alignmentModel->readSentencePairs(sourceFilename, targetFilename, countsFilename, sentRange);
  }

  void swAlignModel_mapSourceWordToWordClass(void* swAlignModelHandle, const char* word, const char* wordClass)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm4AlignmentModel = dynamic_cast<Ibm4AlignmentModel*>(alignmentModel);
    if (ibm4AlignmentModel != nullptr)
      ibm4AlignmentModel->mapSrcWordToWordClass(ibm4AlignmentModel->addSrcSymbol(word), wordClass);
  }

  void swAlignModel_mapTargetWordToWordClass(void* swAlignModelHandle, const char* word, const char* wordClass)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm4AlignmentModel = dynamic_cast<Ibm4AlignmentModel*>(alignmentModel);
    if (ibm4AlignmentModel != nullptr)
      ibm4AlignmentModel->mapTrgWordToWordClass(ibm4AlignmentModel->addTrgSymbol(word), wordClass);
  }

  unsigned int swAlignModel_startTraining(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->startTraining();
  }

  void swAlignModel_train(void* swAlignModelHandle, unsigned int numIters)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    for (unsigned int i = 0; i < numIters; i++)
      alignmentModel->train();
  }

  void swAlignModel_endTraining(void* swAlignModelHandle)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    alignmentModel->endTraining();
  }

  void swAlignModel_save(void* swAlignModelHandle, const char* prefFileName)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    alignmentModel->print(prefFileName);
  }

  double swAlignModel_getTranslationProbability(void* swAlignModelHandle, const char* srcWord, const char* trgWord)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    WordIndex srcWordIndex = alignmentModel->stringToSrcWordIndex(srcWord);
    WordIndex trgWordIndex = alignmentModel->stringToTrgWordIndex(trgWord);
    return alignmentModel->translationProb(srcWordIndex, trgWordIndex);
  }

  double swAlignModel_getTranslationProbabilityByIndex(void* swAlignModelHandle, unsigned int srcWordIndex,
                                                       unsigned int trgWordIndex)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    return alignmentModel->translationProb(srcWordIndex, trgWordIndex);
  }

  double swAlignModel_getIbm2AlignmentProbability(void* swAlignModelHandle, unsigned int j, unsigned int sLen,
                                                  unsigned int tLen, unsigned int i)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto ibm2AlignmentModel = dynamic_cast<Ibm2AlignmentModel*>(alignmentModel);
    if (ibm2AlignmentModel != nullptr)
      return ibm2AlignmentModel->alignmentProb(j, sLen, tLen, i);
    auto faAlignmentModel = dynamic_cast<FastAlignModel*>(alignmentModel);
    if (faAlignmentModel != nullptr)
      return faAlignmentModel->alignmentProb(j, sLen, tLen, i);
    return 0;
  }

  double swAlignModel_getHmmAlignmentProbability(void* swAlignModelHandle, unsigned int prevI, unsigned int sLen,
                                                 unsigned int i)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto hmmAlignmentModel = dynamic_cast<HmmAlignmentModel*>(alignmentModel);
    if (hmmAlignmentModel != nullptr)
      return hmmAlignmentModel->hmmAlignmentProb(prevI, sLen, i);
    return 0;
  }

  double swAlignModel_getBestAlignment(void* swAlignModelHandle, const char* sourceSentence, const char* targetSentence,
                                       bool** matrix, unsigned int* iLen, unsigned int* jLen)
  {
    auto alignmentModel = static_cast<AlignmentModel*>(swAlignModelHandle);

    std::vector<WordIndex> sourceWordIndices = getWordIndices(alignmentModel, sourceSentence, true);
    std::vector<WordIndex> targetWordIndices = getWordIndices(alignmentModel, targetSentence, false);

    WordAlignmentMatrix waMatrix;
    LgProb prob = alignmentModel->getBestAlignment(sourceWordIndices, targetWordIndices, waMatrix);
    for (unsigned int i = 0; i < *iLen; i++)
    {
      for (unsigned int j = 0; j < *jLen; j++)
        matrix[i][j] = waMatrix.getValue(i, j);
    }
    *iLen = waMatrix.get_I();
    *jLen = waMatrix.get_J();
    return prob;
  }

  void* swAlignModel_getTranslations(void* swAlignModelHandle, const char* srcWord, double threshold)
  {
    auto swAligModelPtr = static_cast<AlignmentModel*>(swAlignModelHandle);
    WordIndex srcWordIndex = swAligModelPtr->stringToSrcWordIndex(srcWord);
    auto targetWordsPtr = new NbestTableNode<WordIndex>;
    if (swAligModelPtr->getEntriesForSource(srcWordIndex, *targetWordsPtr) && threshold > 0)
      targetWordsPtr->pruneGivenThreshold(threshold);
    return targetWordsPtr;
  }

  void* swAlignModel_getTranslationsByIndex(void* swAlignModelHandle, unsigned int srcWordIndex, double threshold)
  {
    auto swAligModelPtr = static_cast<AlignmentModel*>(swAlignModelHandle);
    auto targetWordsPtr = new NbestTableNode<WordIndex>;
    if (swAligModelPtr->getEntriesForSource(srcWordIndex, *targetWordsPtr) && threshold > 0)
      targetWordsPtr->pruneGivenThreshold(threshold);
    return targetWordsPtr;
  }

  void swAlignModel_close(void* swAlignModelHandle)
  {
    auto swAligModelPtr = static_cast<AlignmentModel*>(swAlignModelHandle);
    delete swAligModelPtr;
  }

  unsigned int swAlignTrans_getCount(void* swAlignTransHandle)
  {
    auto targetWordsPtr = static_cast<NbestTableNode<WordIndex>*>(swAlignTransHandle);
    return (unsigned int)targetWordsPtr->size();
  }

  unsigned int swAlignTrans_getTranslations(void* swAlignTransHandle, unsigned int* wordIndices, double* probs,
                                            unsigned int capacity)
  {
    auto targetWordsPtr = static_cast<NbestTableNode<WordIndex>*>(swAlignTransHandle);
    if (wordIndices != NULL || probs != NULL)
    {
      NbestTableNode<WordIndex>::iterator iter = targetWordsPtr->begin();
      for (unsigned int i = 0; i < capacity && iter != targetWordsPtr->end(); i++, iter++)
      {
        if (wordIndices != NULL)
          wordIndices[i] = iter->second;
        if (probs != NULL)
          probs[i] = iter->first;
      }
    }
    return (unsigned int)targetWordsPtr->size();
  }

  void swAlignTrans_destroy(void* swAlignTransHandle)
  {
    auto targetWordsPtr = static_cast<NbestTableNode<WordIndex>*>(swAlignTransHandle);
    delete targetWordsPtr;
  }

  bool giza_symmetr1(const char* lhsFileName, const char* rhsFileName, const char* outputFileName, bool transpose)
  {
    AlignmentExtractor alExt;
    if (alExt.open(lhsFileName) == THOT_ERROR)
      return false;
    alExt.symmetr1(rhsFileName, outputFileName, transpose);
    return true;
  }

  bool phraseModel_generate(const char* alignmentFileName, int maxPhraseLength, const char* tableFileName, int n)
  {
    _wbaIncrPhraseModel* phraseModelPtr = new WbaIncrPhraseModel;
    PhraseExtractParameters phePars;
    phePars.maxTrgPhraseLength = maxPhraseLength;
    bool result = phraseModelPtr->generateWbaIncrPhraseModel(alignmentFileName, phePars, false);
    if (result == THOT_OK)
      phraseModelPtr->printTTable(tableFileName, n);
    delete phraseModelPtr;
    return result;
  }

  void* langModel_open(const char* prefFileName)
  {
    BaseNgramLM<LM_State>* lmPtr = new IncrJelMerNgramLM;
    if (lmPtr->load(prefFileName) == THOT_ERROR)
    {
      delete lmPtr;
      return NULL;
    }
    return lmPtr;
  }

  double langModel_getSentenceProbability(void* lmHandle, const char* sentence)
  {
    BaseNgramLM<LM_State>* lmPtr = static_cast<BaseNgramLM<LM_State>*>(lmHandle);
    return lmPtr->getSentenceLog10ProbStr(StrProcUtils::stringToStringVector(sentence));
  }

  void langModel_close(void* lmHandle)
  {
    BaseNgramLM<LM_State>* lmPtr = static_cast<BaseNgramLM<LM_State>*>(lmHandle);
    delete lmPtr;
  }

  void* llWeightUpdater_create()
  {
    auto llwuInfo = new LlWeightUpdaterInfo;
    llwuInfo->baseScorerPtr = new MiraBleu;
    llwuInfo->llWeightUpdaterPtr = new KbMiraLlWu;

    llwuInfo->llWeightUpdaterPtr->link_scorer(llwuInfo->baseScorerPtr);
    return llwuInfo;
  }

  void llWeightUpdater_updateClosedCorpus(void* llWeightUpdaterHandle, const char** references, const char*** nblists,
                                          const double*** scoreComps, const unsigned int* nblistLens, float* weights,
                                          unsigned int numSents, unsigned int numWeights)
  {
    auto llwuInfo = static_cast<LlWeightUpdaterInfo*>(llWeightUpdaterHandle);

    std::vector<std::string> refsVec;
    std::vector<std::vector<std::string>> nblistsVec;
    std::vector<std::vector<std::vector<double>>> scoreCompsVec;
    for (unsigned int i = 0; i < numSents; ++i)
    {
      refsVec.push_back(references[i]);
      std::vector<std::string> nblistVec;
      std::vector<std::vector<double>> nblistScoreCompsVec;
      for (unsigned int j = 0; j < nblistLens[i]; ++j)
      {
        nblistVec.push_back(nblists[i][j]);
        std::vector<double> transScoreCompsVec;
        for (unsigned int k = 0; k < numWeights; ++k)
          transScoreCompsVec.push_back(scoreComps[i][j][k]);
        nblistScoreCompsVec.push_back(transScoreCompsVec);
      }
      nblistsVec.push_back(nblistVec);
      scoreCompsVec.push_back(nblistScoreCompsVec);
    }

    std::vector<double> curWeightsVec;
    for (unsigned int i = 0; i < numWeights; ++i)
      curWeightsVec.push_back(weights[i]);

    std::vector<double> newWeightsVec;
    llwuInfo->llWeightUpdaterPtr->updateClosedCorpus(refsVec, nblistsVec, scoreCompsVec, curWeightsVec, newWeightsVec);

    for (unsigned int i = 0; i < numWeights; ++i)
      weights[i] = (float)newWeightsVec[i];
  }

  void llWeightUpdater_close(void* llWeightUpdaterHandle)
  {
    auto llwuInfo = static_cast<LlWeightUpdaterInfo*>(llWeightUpdaterHandle);
    delete llwuInfo->llWeightUpdaterPtr;
    delete llwuInfo->baseScorerPtr;
    delete llwuInfo;
  }
}
