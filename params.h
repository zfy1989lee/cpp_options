#include <iostream>
#include <string>

class c_params{
 public:
  c_params(std::string);
  ~c_params();

  std::string database_name;
  std::string user_name;
  std::string password;
  std::string host;
  std::string table_name;
  unsigned int threshold;
  unsigned int num_cycles;
  double linear_delta_width;
  double min_ytm;
  double manual_rebalancing_delta_fraction;
  std::string conf_file_name;
  std::string folder_name;
};

c_params::c_params(std::string conf_file){
  FILE *pFile = fopen(conf_file.c_str(), "r");

  if(pFile!=NULL){
    char line[256];

    fscanf(pFile,"%s\n",line);
    this->database_name = std::string(line);

    fscanf(pFile,"%s\n",line);
    this->user_name = std::string(line);

    fscanf(pFile,"%s\n",line);
    this->password = std::string(line);

    fscanf(pFile,"%s\n",line);
    this->host = std::string(line);

    fscanf(pFile,"%s\n",line);
    this->table_name = std::string(line);

    fscanf(pFile,"%s\n",line);
    this->threshold = std::stoi(std::string(line));

    fscanf(pFile,"%s\n",line);
    this->num_cycles = std::stoi(std::string(line));

    fscanf(pFile,"%s\n",line);
    this->linear_delta_width = std::stod(std::string(line));

    fscanf(pFile,"%s\n",line);
    this->min_ytm = std::stod(std::string(line));

    fscanf(pFile,"%s\n",line);
    this->manual_rebalancing_delta_fraction = std::stod(std::string(line));

    fclose(pFile);

    this->conf_file_name = conf_file;
    this->folder_name = conf_file;

    unsigned int pos1 = this->folder_name.rfind("/");    
    if(pos1!=std::string::npos){
      this->folder_name = this->folder_name.substr(pos1+1,this->folder_name.size()-pos1+1);
    }

    unsigned int pos2 = this->folder_name.rfind(".");
    if(pos2!=std::string::npos){
      this->folder_name = this->folder_name.substr(0,pos2);
    }

    this->folder_name = "reports/"+this->folder_name;
  }
  else{
    std::cout<<("Cannot open file "+conf_file)<<std::endl;
  }
}

c_params::~c_params(){}

