Newspapers Front pages
================

Python 3.x scripts to download newspapers front pages.

##Getting started

###1. Open the config.txt file and configure your settings

* <em><b>root_dir</b></em>: the root path that is used to store the downloaded covers.
* <em><b>share_src</b></em>: a boolean, true or false, that defines if the downloaded images goes to the <b>root_dir</b> (if boolean true) or to a specifc folder ( <b>root_dir</b> +  <b>newspaper_dir</b>) define by to the newspaper;
* <em>config.txt sample:</em>
	
		root_dir=/Users/jbatista/Pictures/newspapers/x/
		share_src=false
	
		# folders, only used if share_src is not true
		Correio da Manhã=news/
		Público=news/
		Jornal de Notícias=news/
		Jornal i=news/
		Diário de Notícias=news/
		O Primeiro de Janeiro=news/
		Diário Económico=news/
		A Bola=sports/
		Record=sports/
		O Jogo=sports/


###2. Run one of the follow scripts:

	$ ./portugal_newspapers.py
	$ ./abola.py

## portugal_newspapers.py
Download today's front pages from <a href="http://www.tvtuga.pt">tvtuga</a> of the following newspapers:
* Correio da Manhã
* Público
* Jornal de Notícias
* Jornal i
* Diário de Notícias
* O Primeiro de Janeiro
* Diário Económico
* A Bola
* Record
* O Jogo

## abola.py
Download <a href="http://www.abola.pt/" title="abola">A Bola</a> front pages of the last seven days

#Authors
<b>Jóni Batista</b>
* https://github.com/jonibatista
* https://twitter.com/jonibatista

##License
Copyright &copy; 2012 Jóni Batista.

Licensed under the GNU General Public License (GPL), Version 3.0.

You may obtain a copy of the License in the LICENSE file, or at:
http://www.gnu.org/licenses/gpl.html

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
