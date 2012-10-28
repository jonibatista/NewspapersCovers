NewspapersCovers
================

Python 3.x script to download newspapers covers.

The script will get the last cover downloaded in the path that you specify (config.txt file) and it calulates the missing covers, then the covers available are downloaded.

##Getting started

###1. Open the config.txt file and configure your settings

* <em><b>root_dir</b></em>: the root path that is used to store the downloaded covers. Depending on the <em>share_src</em> and <em>src</em> is added a folder to complete the path; 
* <em><b>share_src</b></em>: a boolean that defines if all newspapers covers are placed in the same flolder (true) or in a different folder for each newspaper (the folder names is the name of the newspaper);
* <em><b>src</b></em>: it defines the name of the shared folder for which all images are downloaded. This it's only used when the <em>share_src</em> parameter is set to true.


###2. Run the script of which newspaper you want, such as:

	`$ ./abola.py`


##Available
* <a href="http://www.abola.pt/" title="abola">abola</a>
* <a href="http://www.record.xl.pt/" title="record">record</a>


##Workin on
* what's next?

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