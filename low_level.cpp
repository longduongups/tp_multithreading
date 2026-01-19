#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

#include <iostream>
#include <vector>

int main() {
  using json = nlohmann::json;

  // Construire une Task JSON
  // Laisser a/b/x dans le JSON pour coller à Task.from_json en Python
  json task;
  task["identifier"] = 42;
  task["size"] = 50;
  task["a"] = json::array(); // laissé vide
  task["b"] = json::array();
  task["x"] = json::array();
  task["time"] = 0.0;

  // POST -> soumettre la tâche
  auto post =
      cpr::Post(cpr::Url{"http://127.0.0.1:8000/"}, cpr::Body{task.dump()},
                cpr::Header{{"Content-Type", "application/json"}});

  std::cout << "POST status_code: " << post.status_code << "\n";
  std::cout << "POST response: " << post.text << "\n";

  // GET -> récupérer le résultat
  auto rget = cpr::Get(cpr::Url{"http://127.0.0.1:8000/"});
  std::cout << "GET status_code: " << rget.status_code << "\n";
  std::cout << "GET response: " << rget.text << "\n";

  // Parser le JSON résultat
  json result = json::parse(get.text);
  std::cout << "Result:\n" << result.dump(2) << "\n";

  // Afficher des infos
  std::cout << "identifier=" << result["identifier"] << "\n";
  std::cout << "size=" << result["size"] << "\n";
  std::cout << "time=" << result["time"] << " s\n";

  return 0;
}
